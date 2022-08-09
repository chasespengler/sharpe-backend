'''
Holds functions necessary to calculate certain financial metrics
'''
from statistics import mean
import yfinance as yf

def expected_return(ticker):
    '''
    Returns the expected return of a security
    args: ticker (str, takes the ticker of a security)
    '''
    pass

'''
tick = yf.download(['AAPL', 'GOOG']).Close.pct_change().dropna()

print(tick.columns)

for x in tick.columns:
    print(x)
    print(tick[x].head().values)
'''

