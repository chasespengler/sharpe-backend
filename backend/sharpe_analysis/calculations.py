'''
Holds functions necessary to calculate certain financial metrics
'''
from statistics import mean
import yfinance as yf

def calc_sharpe(eq_data, port_data):
    '''
    Returns the sharpe ratio of a portfolio
    args: eq_data (dictionary of json, takes the relevant input data in the following format:
    {
        'SPY':
            {
                'ticker':'SPY',
                'mean': 0.5,
                'sd': 0.15,
                'cur_price': 100,
            }
    }
    )
    '''
    pass

'''
tick = yf.download(['AAPL', 'GOOG']).Close.pct_change().dropna()

print(tick.columns)

for x in tick.columns:
    print(x)
    print(tick[x].head().values)
'''

