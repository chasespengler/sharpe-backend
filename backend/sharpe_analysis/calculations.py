'''
Holds functions necessary to calculate certain financial metrics
'''
from statistics import mean
import yfinance as yf

def calc_sharpe(eq_data, port_data):
    '''
    Returns the sharpe ratio of a portfolio
    args: eq_data (equity data, dictionary of json, takes the relevant input data in the following format:
    {
        'SPY':
            {
                'ticker':'SPY',
                'mean': 0.5,
                'sd': 0.15,
                'cur_price': 100,
            },
    }
    )

        port_data (portfolio data, list of dictionaries, takes the relevant input data in the following format:
        [
        {'id': 22, 
        'security_type': 'Equity', 
        'ticker': 'DAX', 
        'amount': 5.0, 
        'portfolio_parent_id': 35},
        ]
        )
    '''
    
    ##### CHANGE HARD CODED RISK FREE RATE ######
    rf_rate = 0.05 /250
    port_value = 0

    #Needed to find total value of portfolio for weights of each allocation
    for sec in port_data:
        if sec['security_type'] == 'Equity':
            port_value += sec['amount'] * eq_data[sec['ticker']]['cur_price']

    port_ev_return = 0
    port_var_return = 0
    port_down_var = 0

    #Needed to initialize the weight of the first security
    port_data[0]['weight'] = port_data[0]['amount'] * eq_data[port_data[0]['ticker']]['cur_price'] / port_value
    
    #Calculating variance of portfolio and expected return
    for i in range(len(port_data)):
        sec = port_data[i]
        sec_data = eq_data[sec['ticker']]
        sec_weight = sec['weight']
        port_ev_return += sec['amount'] * sec_data['cur_price'] * sec_data['mean']
        port_var_return += (sec_weight ** 2) * (sec_data['sd'] ** 2)
        port_down_var += (sec_weight ** 2) * (sec_data['down_sd'] ** 2)

        #Covariance
        for z in range(i + 1, len(port_data)):
            other_sec = port_data[z]
            other_data = eq_data[other_sec['ticker']]
            if i == 0:
                port_data[z]['weight'] = other_sec['amount'] * other_data['cur_price'] / port_value

            port_var_return += 2 * sec_weight * other_sec['weight'] * sec_data['sd'] * other_data['sd']
            port_down_var += 2 * sec_weight * other_sec['weight'] * sec_data['down_sd'] * other_data['down_sd']

    port_ev_return = port_ev_return / port_value
    port_sd_return = port_var_return ** 0.5
    port_down_sd = port_down_var ** 0.5

    sharpe = (port_ev_return - rf_rate) / port_sd_return
    sortino = (port_ev_return - rf_rate) / port_down_sd if port_down_sd else 0.0
    value_at_risk = port_value * (2.33 * port_sd_return)
    return round(sharpe, 4), round(sortino, 4), round(value_at_risk, 2), port_value



'''
tick = yf.download(['AAPL', 'GOOG']).Close.pct_change().dropna()

print(tick.columns)

for x in tick.columns:
    print(x)
    print(tick[x].head().values)
'''

