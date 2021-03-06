# Moving average crossover
A simple script to backtest the moving average crossover strategy

##### A sample Moving average and price graph of Microsoft with buy and sell signals between 2007-01-01 and 2017-12-31

![signals_with_ma](https://user-images.githubusercontent.com/18646185/87329901-5eb47c00-c555-11ea-97cd-123fb50ad8d6.png)

##### A sample portfolio graph (Microsoft only) with buy and sell signals between 2007-01-01 and 2017-12-31 starting with a capital of 100000

![portfolio](https://user-images.githubusercontent.com/18646185/87329897-5d834f00-c555-11ea-83dc-196f56fc5fc3.png)

## Getting Started

Clone the repository and navigate to the project directory

```
git clone https://github.com/Arutselvan/moving_average_crossover
cd moving_average_crossover
```

### Prerequisites

Make sure you have python 3.5 or above installed

Install tkinter before installing the dependencies (for Matplotlib)
```
sudo apt-get install python3-tk
```

### Installing dependencies

```
python3 -m pip install -r requirements.txt
```

## Usage
```
usage: ma_crossover.py [-h] --ticker TICKER --start_date START_DATE --end_date END_DATE [--short_window SHORT_WINDOW] [--long_window LONG_WINDOW] [--capital CAPITAL]
                       [--stocks_per_trade STOCKS_PER_TRADE]

optional arguments:
  -h, --help            show this help message and exit
  --ticker TICKER       The ticker for which you want test the moving average crossover strategy
  --start_date START_DATE
                        Start date (YYYY-MM-DD) (must be earlier than the current date)
  --end_date END_DATE   End date (YYYY-MM-DD) (must be earlier or equal to the current date)
  --short_window SHORT_WINDOW
                        Size of the short window (in days)
  --long_window LONG_WINDOW
                        Size of the long window (in days)
  --capital CAPITAL     Starting capital amount
  --stocks_per_trade STOCKS_PER_TRADE
                        Number of stocks traded per buy/sell trade
```

Example
```
python ma_crossover.py --ticker='MSFT' --start_date='2007-01-01' --end_date='2017-12-31'
```

Example with custom capital value
```
python ma_crossover.py --ticker='AAPL' --start_date='2007-01-01' --end_date='2017-12-31' --capital=250000
```

## To Do
- Add support for multiple tickers
