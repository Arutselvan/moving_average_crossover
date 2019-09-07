import argparse
import pandas as pd
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class MovingAverageCrossover:

    def __init__(self, ticker, capital, stocks_per_trade, start_date, end_date, short_window, long_window):
        self.ticker = ticker
        self.capital = capital
        self.stocks_per_trade = stocks_per_trade
        self.start_date = start_date
        self.end_date = end_date
        self.short_window = short_window
        self.long_window = long_window

    def get_data(self):
        self.stock_data = data.DataReader(ticker,'yahoo',start_date,end_date) # get data from yahoo finance
        self.close_price = self.stock_data['Close'] # get the closing prices

        """ Get all weekdays and fill dates with latest price when price is not available """

        all_weekdays = pd.date_range(start=self.start_date, end=self.end_date, freq='B') 
        self.close_price = self.close_price.reindex(all_weekdays)
        self.close_price = self.close_price.fillna(method='ffill')

    def calc_ma(self):

        """ Function to calculate moving averages """

        self.sma = self.close_price.rolling(window=self.short_window).mean() # calculate short term moving average
        self.lma = self.close_price.rolling(window=self.long_window).mean() # calculate long term moving average

    def generate_signals(self):

        """ Generate buy and sell trade signals """
        self.close_price_temp = self.close_price.shift(1) # to remove look ahead bias shift closing prices by 1 day
        self.signals = pd.DataFrame(index=self.close_price_temp.index)
        self.signals['signal'] = 0.0
        self.sma_temp = self.close_price_temp.rolling(window=self.short_window).mean() # calculate short term moving average with shifted values
        self.lma_temp = self.close_price_temp.rolling(window=self.long_window).mean() # calculate long time moving average with shifted values
        self.signals['signal'][self.short_window:] = np.where(self.sma_temp[self.short_window:]>self.lma_temp[self.short_window:],1.0,0.0) #1 when short term average is greater than long term average
        self.signals['positions'] = self.signals['signal'].diff() # diff will give 1 (buy signal) when sma crosses lma and -1 (sell) when lma crosses sma

    def plot_signals_with_ma(self):

        """ Plot short term and long term moving average with closing price and trade signals """ 

        fig,ax = plt.subplots(figsize=(20,15))
        ax.plot(self.close_price.index,self.close_price, label="Price")
        ax.plot(self.sma.index, self.sma, label="50 days moving average")
        ax.plot(self.lma.index, self.lma, label="200 days moving average")
        ax.plot(self.signals.loc[self.signals.positions == 1.0].index, self.sma[self.signals.positions == 1.0], '^', markersize=10, color='g', label="Buy signal")
        ax.plot(self.signals.loc[self.signals.positions == -1.0].index, self.sma[self.signals.positions == -1.0], 'v', markersize=10, color='r', label="Sell signal")
        ax.set_xlabel('Date')
        ax.set_ylabel('Adjusted closing price')
        ax.set_title('Moving average crossover plot with buy and sell signals')
        ax.legend()
        plt.savefig('signals_with_ma.png')
        #plt.show()

    def backtest_portfolio(self):

        """ Backtesting the portfolio with initial capital equal to the specified amount """

        self.positions = pd.DataFrame(index=self.signals.index).fillna(0.0)
        self.positions['positioninrs'] = self.stocks_per_trade*self.signals['signal'] # each position has stocks equal to stocks per trade specified
        self.portfolio = self.positions.multiply(self.close_price, axis=0) # multiply positions with stock price on that day to get value
        self.pos_diff = self.positions.diff()
        self.portfolio['holdings'] = (self.positions.multiply(self.close_price,axis=0)).sum(axis=1) # total amount in holdings
        self.portfolio['cash'] = self.capital - (self.pos_diff.multiply(self.close_price,axis=0)).sum(axis=1).cumsum() # total in cash
        self.portfolio['total'] = self.portfolio['cash'] + self.portfolio['holdings'] # total value
        self.portfolio['returns'] = self.portfolio['total'].pct_change() # returns as percentage change
        del self.portfolio['positioninrs']

    def plot_portfolio(self):

        """ Function for plotting the portfolio value graph """

        fig = plt.figure(figsize=(20,15))
        ax = fig.add_subplot(111,ylabel="Portfolio_value", xlabel="Date",title = "Portfolio Plot")
        ax.plot(self.portfolio['total'].index, self.portfolio['total'], label = "Portfolio value")
        ax.plot(self.portfolio.loc[self.signals.positions == 1.0].index, self.portfolio.total[self.signals.positions==1.0], '^', markersize=10, color='g', label = "Bought")
        ax.plot(self.portfolio.loc[self.signals.positions == -1.0].index, self.portfolio.total[self.signals.positions==-1.0], 'v', markersize=10, color='r', label = "Sold")
        ax.legend()
        plt.savefig('portfolio.png')
        #plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', help="The ticker for which you want test the moving average crossover strategy", required=True)
    parser.add_argument('--start_date',help="Start date (YYYY-MM-DD) (must be earlier than the current date)", required=True)
    parser.add_argument('--end_date',help="End date (YYYY-MM-DD) (must be earlier or equal to the current date)", required=True)
    parser.add_argument('--short_window',type=int,help="Size of the short window (in days)", default=50)
    parser.add_argument('--long_window',type=int,help="Size of the long window (in days)", default=200)
    parser.add_argument('--capital',type=int,help="Starting capital amount", default=100000)
    parser.add_argument('--stocks_per_trade',type=int,help="Number of stocks traded per buy/sell trade", default=100)
    args = parser.parse_args()

    ticker = args.ticker
    start_date = args.start_date
    end_date = args.end_date
    short_window = args.short_window
    long_window = args.long_window
    capital = args.capital
    stocks_per_trade = args.stocks_per_trade


    mvac = MovingAverageCrossover(ticker, capital, stocks_per_trade, start_date, end_date, short_window, long_window)
    mvac.get_data()
    mvac.calc_ma()
    mvac.generate_signals()
    mvac.backtest_portfolio()
    mvac.plot_signals_with_ma()
    mvac.plot_portfolio()

    print("Portfolio total value on Dec 29, 2017 in Rs")
    print(mvac.portfolio['total'].tail(1))  # get portfolio value on the last working day

    print("Absolute return as of Dec 29, 2017 in Rs")
    print(mvac.portfolio['total'].tail(1) - mvac.capital) # Total returns


