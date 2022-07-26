"""
Tests for SharpeCache behavior.
"""
import unittest

import pandas as pd
from sharpe.analysis.analysis.data.cache import SharpeCache


class TestResampleDataframe(unittest.TestCase):
    def test_put_get_no_compute(self):
        """Tests that DataFrames are unchanged when period and interval conditions are already met."""
        df = get_yahoo_data_daily_over_one_year()
        cache: SharpeCache = SharpeCache()
        interval = "1d"
        period = "1y"

        cache.put("IBM", interval, period, df)
        _df = cache.get("IBM", interval, period)
        self.assertIsNotNone(_df)
        self.assertEqual(id(_df), id(df))

    def test_put_get_interval_computed(self):
        """Tests that DataFrame's data points are reduced when interval must be computed from
        cached data.
        """
        df = get_yahoo_data_daily_over_one_year()
        cache: SharpeCache = SharpeCache()
        interval_1, interval_2 = "1d", "1wk"
        period = "1y"

        cache.put("IBM", interval_1, period, df)
        _df = cache.get("IBM", interval_2, period)
        self.assertIsNotNone(_df)
        self.assertAlmostEqual(len(_df), 52, places=-1)

    def test_put_get_period_computed(self):
        """Tests that DataFrame's data points are reduced when period must be truncated from
        cached data.
        """
        df = get_yahoo_data_daily_over_one_year()
        cache: SharpeCache = SharpeCache()
        interval = "1d"
        period_1, period_2 = "1y", "6mo"

        cache.put("IBM", interval, period_1, df)
        _df = cache.get("IBM", interval, period_2)
        self.assertIsNotNone(_df)
        self.assertEqual(len(_df), 180)

    def test_put_get_interval_and_period_computed(self):
        """Tests that DataFrame's data points are reduced when interval must be computed from
        cached data.
        """
        df = get_yahoo_data_daily_over_one_year()
        cache: SharpeCache = SharpeCache()
        interval_1, interval_2 = "1d", "1wk"
        period_1, period_2 = "1y", "6mo"

        cache.put("IBM", interval_1, period_1, df)
        _df = cache.get("IBM", interval_2, period_2)
        self.assertIsNotNone(_df)
        self.assertAlmostEqual(len(_df), 24, places=-1)

    def test_put_get_interval_and_period_no_compute_available(self):
        """Tests that cache cannot compute from existing data."""
        df = get_yahoo_data_daily_over_one_year()
        cache: SharpeCache = SharpeCache()
        interval_1, interval_2 = "1d", "1wk"
        period_1, period_2 = "1y", "2y"

        cache.put("IBM", interval_1, period_1, df)
        _df = cache.get("IBM", interval_2, period_2)
        self.assertIsNone(_df)


def get_yahoo_data_daily_over_one_year():
    df = pd.read_csv(
        "tests/test_data/yahoo_finance_IBM_period-1y_interval-1d.csv", infer_datetime_format=True
    )
    df["Date"] = pd.to_datetime(df["Date"], infer_datetime_format=True)

    df = df.rename(columns={"Open": "price", "Dividends": "dividend"})

    # This is here because sometiems rows are exclusively dividend rows, while others are
    # price rows. A date can have one price, one dividend, or one of each. Group and sum the
    # dividends
    df = df.groupby("Date", axis=0, as_index=True).agg({"price": "mean", "dividend": "sum"})
    df.drop(columns=[c for c in df.columns if c not in ("price", "dividend")], inplace=True)
    return df


def get_yahoo_data_monthly_over_five_years():
    df = pd.read_csv(
        "tests/test_data/yahoo_finance_IBM_period-5y_interval-1mo.csv", infer_datetime_format=True
    )
    df["Date"] = pd.to_datetime(df["Date"], infer_datetime_format=True)

    # This is here because some rows are exclusively dividend rows, while others are
    # price rows. A date will have one price, one dividend, or one of each. Group
    # and sum the dividends
    df = df.groupby("Date", axis=0, as_index=True).sum()
    df = df.rename(columns={"Open": "price", "Dividends": "dividend"})
    df.drop(columns=[c for c in df.columns if c not in ("price", "dividend")], inplace=True)
    return df
