'''
Holds functions necessary to retrieve relevant financial data and update databases accordingly
'''
import yfinance as yf
from statistics import mean, stdev
import requests

r = 'http://127.0.0.1:8000/'

def ticker_is_real(tick):
    '''
    Returns the status of a ticker's existence
    '''
    if yf.download(tick).empty:
        return False
    return True

def add_eq_data(tickers):
    '''
    Adds new equity data
    '''
    data = yf.download(tickers).Close
    cur_price = data.iloc[-1]
    if len(tickers) == 1:
        d = data.pct_change().dropna().values
        ev = mean(d)
        sd = stdev(d)
        down_sd = (sum(((d[(d < 0)] - ev) ** 2)) / len(d)) ** 0.5
        print(sd, down_sd)
        js = {
            "ticker": tickers[0],
            "mean": ev,
            "sd": sd,
            "cur_price": cur_price,
            "down_sd": down_sd,
        }
        requests.post(r + 'api/post-stats/', js)
    else:
        cols = data.columns
        for col in cols:
            d = data[col].dropna().values
            ev = mean(d)
            sd = stdev(d)
            down_sd = (sum(((d[(d < 0)] - ev) ** 2)) / len(d)) ** 0.5
            js = {
                "ticker": col,
                "mean": ev,
                "sd": sd,
                "cur_price": d[-1],
                "down_sd": down_sd,
            }
            requests.post(r + 'api/post-stats/', js)

def update_eq_data(tickers):
    '''
    Updates existing equity data
    '''
    data = yf.download(tickers).Close
    cur_price = data.iloc[-1]
    if len(tickers) == 1:
        d = data.pct_change().dropna().values
        ev = mean(d)
        sd = stdev(d)
        down_sd = (sum(((d[(d < 0)] - ev) ** 2)) / len(d)) ** 0.5
        js = {
            "ticker": tickers[0],
            "mean": ev,
            "sd": sd,
            "cur_price": cur_price,
            "down_sd": down_sd,
        }
        requests.post(r + 'api/update-stats/' + str(tickers[0]) + '/', js)
    else:
        cols = data.columns
        for col in cols:
            d = data[col].dropna().values
            ev = mean(d)
            sd = stdev(d)
            down_sd = (sum(((d[(d < 0)] - ev) ** 2)) / len(d)) ** 0.5
            js = {
                "ticker": col,
                "mean": ev,
                "sd": sd,
                "cur_price": d[-1],
                "down_sd": down_sd,
            }
            requests.post(r + 'api/update-stats/' + str(col) + '/', js)

def update_and_add_eq(tickers):
    '''
    Adds and updates equity data
    '''
    add, update = needs_adding(tickers)
    
    if update:
        update_eq_data(update)
    if add:
        add_eq_data(add)

def get_eq_data(tickers):
    '''
    Retrieves equity data from api
    '''
    data = {}
    for tick in tickers:
        data[tick] = requests.get(r + 'api/get-stats/' + tick + '/').json()

    return data

def needs_adding(tickers):
    '''
    Returns tickers that need to be added to equity stats database and those that already exist, respectively
    '''
    add = []
    update = []
    for tick in tickers:
        if requests.get(r + 'api/exists/' + tick + '/').text == 'true':
            update.append(tick)
        else:
            add.append(tick)

    return add, update