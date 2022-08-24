import unittest
from django.test import TestCase
from calculations import calc_sharpe
import unittest

# Create your tests here.

class TestCalculations(unittest.TestCase):

    def test_sharpe(self):
        eq_data = {
            'SPY':
            {
                'ticker':'SPY',
                'mean': 0.5,
                'sd': 0.15,
                'cur_price': 100,
            },
            'VOO':
            {
                'ticker':'VOO',
                'mean': 0.25,
                'sd': 0.10,
                'cur_price': 120,
            },
            'QQQ':
            {
                'ticker':'QQQ',
                'mean': 0.1,
                'sd': 0.2,
                'cur_price': 80,
            },
        }
        port_data = [
            {
                'id': 22,
                'security_type': 'Equity',
                'ticker': 'SPY',
                'amount': 5,
                'portfolio_parent_id': 1,
            },
            {
                'id': 23,
                'security_type': 'Equity',
                'ticker': 'VOO',
                'amount': 4,
                'portfolio_parent_id': 1,
            },
            {
                'id': 24,
                'security_type': 'Equity',
                'ticker': 'QQQ',
                'amount': 6,
                'portfolio_parent_id': 1,
            },
        ]
        eq_data1 = {
            'SPY':
            {
                'ticker':'SPY',
                'mean': 0.05 / 250,
                'sd': 0.15,
                'cur_price': 100,
            },
            'VOO':
            {
                'ticker':'VOO',
                'mean': 0.05 / 250,
                'sd': 0.10,
                'cur_price': 100,
            },
            'QQQ':
            {
                'ticker':'QQQ',
                'mean': 0.05 / 250,
                'sd': 0.2,
                'cur_price': 100,
            },
        }
        port_data1 = [
            {
                'id': 22,
                'security_type': 'Equity',
                'ticker': 'SPY',
                'amount': 5,
                'portfolio_parent_id': 1,
            },
            {
                'id': 23,
                'security_type': 'Equity',
                'ticker': 'VOO',
                'amount': 5,
                'portfolio_parent_id': 1,
            },
            {
                'id': 24,
                'security_type': 'Equity',
                'ticker': 'QQQ',
                'amount': 5,
                'portfolio_parent_id': 1,
            },
        ]
        eq_data2 = {
            'SPY':
            {
                'ticker':'SPY',
                'mean': 0.05,
                'sd': 1,
                'cur_price': 100,
            },
            'QQQ':
            {
                'ticker':'QQQ',
                'mean': 0.05,
                'sd': 1,
                'cur_price': 100,
            },
        }
        port_data2 = [
            {
                'id': 22,
                'security_type': 'Equity',
                'ticker': 'SPY',
                'amount': 5,
                'portfolio_parent_id': 1,
            },
            {
                'id': 23,
                'security_type': 'Equity',
                'ticker': 'QQQ',
                'amount': 5,
                'portfolio_parent_id': 1,
            },
        ]
        self.assertAlmostEqual(calc_sharpe(eq_data, port_data), 1.907342478, delta=0.0000001)
        self.assertAlmostEqual(calc_sharpe(eq_data1, port_data1), 0, delta=0.0000001)

if __name__ == '__main__':
    unittest.main()