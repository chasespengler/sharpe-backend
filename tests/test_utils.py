"""
Tests for utility functions.

"""
import logging
import unittest

import pandas as pd
import requests
from sharpe.analysis import utils
from sharpe.analysis.timestring import TimeString


class TestResampleDataframe(unittest.TestCase):
    def test_same_interval_same_period(self):
        """Tests that DataFrames are unchanged when period and interval conditions are already met."""
        df = get_yahoo_data_daily_over_one_year()

        _df = utils.resample_dataframe_to_period_interval(
            df, interval=TimeString("1d"), period=TimeString("1y")
        )
        self.assertAlmostEqual(len(_df), 365, places=-1)

    def test_same_interval_different_period_truncated(self):
        """Tests that DataFrame intervals are unchanged but, assuming roughly equidistant rows,
        the number of data points is cut in half.
        """
        df = get_yahoo_data_daily_over_one_year()

        _df = utils.resample_dataframe_to_period_interval(
            df, interval=TimeString("1d"), period=TimeString("6mo")
        )
        self.assertAlmostEqual(len(_df), 183, places=-1)

    def test_same_interval_different_period_not_truncated(self):
        """Tests that DataFrame intervals are unchanged and, because the new period is longer than
        the DataFrame's own, the number of data points are unchanged as well.
        """
        df = get_yahoo_data_daily_over_one_year()

        _df = utils.resample_dataframe_to_period_interval(
            df, interval=TimeString("1d"), period=TimeString("2y")
        )
        # Should not expand or trim
        self.assertAlmostEqual(len(_df), 365, places=-1)

    def test_different_interval_same_period(self):
        """Tests that DataFrame intervals change but the period does not."""
        df = get_yahoo_data_daily_over_one_year()

        _df = utils.resample_dataframe_to_period_interval(
            df, interval=TimeString("1wk"), period=TimeString("1y")
        )
        self.assertAlmostEqual(len(_df), 52, places=-1)

    def test_different_interval_different_period_truncated(self):
        """Tests that DataFrame intervals change and the number of data points is halved."""
        df = get_yahoo_data_daily_over_one_year()

        _df = utils.resample_dataframe_to_period_interval(
            df, interval=TimeString("1wk"), period=TimeString("6mo")
        )
        self.assertAlmostEqual(len(_df), 26, places=-1)

    def test_different_interval_different_period_not_truncated(self):
        """Tests that DataFrame intervals change and, because the new period is longer than
        the DataFrame's own, the number of data points are unchanged as well.
        """
        df = get_yahoo_data_daily_over_one_year()

        _df = utils.resample_dataframe_to_period_interval(
            df, interval=TimeString("1wk"), period=TimeString("2y")
        )
        self.assertAlmostEqual(len(_df), 52, places=-1)


class TestRetry(unittest.TestCase):
    def test_error(self):
        """Tests the retry wrappers ability to log retries and errors and throw after the limit is met."""
        logger = logging.getLogger("null")

        @utils.retry(3, exception=ZeroDivisionError, logger=logger)
        def divide_by_zero(x: int):
            return x / 0

        with self.assertRaises(ZeroDivisionError), self.assertLogs(
            logger, level=logging.DEBUG
        ), self.assertLogs(logger, level=logging.ERROR):
            divide_by_zero(1)

        @utils.retry(0, exception=requests.ConnectionError, logger=logger)
        def timeout_error():
            requests.get("https://localhost:0000/a/non-existant/path")

        with self.assertRaises(requests.ConnectionError), self.assertLogs(
            logger, level=logging.ERROR
        ):
            timeout_error()

    def test_successful_retry(self):
        """Tests that the wrapped function returns a correct result after failing at least once."""
        logger = logging.getLogger("null")

        @utils.retry(3, exception=ZeroDivisionError, logger=logger)
        def get_inverse(_range):
            return -1 / next(_range)

        with self.assertLogs(logger, level=logging.DEBUG):
            # Should fail on the first value (0), and succeed on the second (1)
            inverse = get_inverse(iter(range(2)))

        self.assertEqual(inverse, -1)

    def test_successful_initial(self):
        """Tests that the wrapped function returns a correct result the first time without appending
        logs or raising errors.
        """
        logger = logging.Logger(__name__)

        @utils.retry(3, exception=ZeroDivisionError, logger=logger)
        def get_half(x):
            return x / 2

        with self.assertLogs(logger, level=logging.DEBUG) as cm:
            logger.debug("Dummy")
            half = get_half(1)

        self.assertEqual(half, 0.5)
        # Assert that this is the only log made
        self.assertListEqual([f"DEBUG:{__name__}:Dummy"], cm.output)


def get_yahoo_data_daily_over_one_year():
    df = pd.read_csv(
        "tests/test_data/yahoo_finance_IBM_period-1y_interval-1d.csv", infer_datetime_format=True
    )
    df["Date"] = pd.to_datetime(df["Date"], infer_datetime_format=True)

    # This is here because some rows are exclusively dividend rows, while others are
    # price rows. A date will have one price, one dividend, or one of each. Group
    # and sum the dividends
    df = df.groupby("Date", axis=0, as_index=True).sum()
    df = df.rename(columns={"Open": "price", "Dividends": "dividend"})
    df.drop(columns=[c for c in df.columns if c not in ("price", "dividend")], inplace=True)
    return df
