import pandas as pd
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ticker = 'INFY.NS'

start_date = '2007-01-01'
end_date = '2017-12-31'

short_window = 50 
long_window = 200

stock_data = data.DataReader(ticker,'yahoo',start_date,end_date) #get data from yahoo finance

close_price = stock_data['Close'] #get the closing prices

all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B') 

close_price = close_price.reindex(all_weekdays)

close_price = close_price.fillna(method='ffill')

sma = close_price.rolling(window=short_window).mean()
lma = close_price.rolling(window=long_window).mean()

signals = pd.DataFrame(index=close_price.index)

signals['signal'] = 0.0

signals['signal'][short_window:] = np.where(sma[short_window:]>lma[short_window:],1.0,0.0)

signals['positions'] = signals['signal'].diff()

fig,ax = plt.subplots(figsize=(20,15))

ax.plot(close_price.index,close_price, label="Price")
ax.plot(sma.index, sma, label="50 days moving average")
ax.plot(lma.index, lma, label="200 days moving average")
ax.plot(signals.loc[signals.positions == 1.0].index, sma[signals.positions == 1.0], '^', markersize=10, color='g', label="Buy signal")
ax.plot(signals.loc[signals.positions == -1.0].index, sma[signals.positions == -1.0], 'v', markersize=10, color='r', label="Sell signal")
ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price')
ax.legend()
plt.show()

initial_capital = 100000

positions = pd.DataFrame(index=signals.index).fillna(0.0)

shares_per_trade = 100

positions['positioninrs'] = shares_per_trade*signals['signal']

portfolio = positions.multiply(close_price, axis=0)

pos_diff = positions.diff()

portfolio['holdings'] = (positions.multiply(close_price,axis=0)).sum(axis=1)

portfolio['cash'] = initial_capital - (pos_diff.multiply(close_price,axis=0)).sum(axis=1).cumsum()

portfolio['total'] = portfolio['cash'] + portfolio['holdings']

portfolio['returns'] = portfolio['total'].pct_change()

del portfolio['positioninrs']

print(portfolio.tail())

#print(portfolio.tail())

fig = plt.figure(figsize=(20,15))
ax = fig.add_subplot(111,ylabel="Portfolio_value")
ax.plot(portfolio['total'].index, portfolio['total'], label = "Portfolio value")
ax.plot(portfolio.loc[signals.positions == 1.0].index, portfolio.total[signals.positions==1.0], '^', markersize=10, color='g', label = "Bought")
ax.plot(portfolio.loc[signals.positions == -1.0].index, portfolio.total[signals.positions==-1.0], 'v', markersize=10, color='r', label = "Sold")
# print(portfolio['total'].tail())

ax.legend()

plt.show()