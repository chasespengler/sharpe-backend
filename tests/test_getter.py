"""
Tests for concrete DataGetter implementations.
"""
import abc
import unittest
from typing import Optional

import numpy as np
import pandas as pd
from sharpe.analysis.analysis.data import data_getter_factory


class DataGetter(unittest.TestCase, metaclass=abc.ABCMeta):
    def assertValidDataFrame(
        self, df: pd.DataFrame, length: Optional[int] = None, length_places: Optional[int] = None
    ):
        """Asserts that a DataFrame meets the caller's expectations.

        :param df: DataFrame that caller would be using
        :param length: Length the DataFrame ought to be, defaults to None
        :param length_places: Number of decimal places the DataFrame's length can vary by, defaults to None
        """
        self.assertListEqual(df.columns.to_list(), ["price", "dividend"])
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        self.assertEqual(df["price"].dtype, np.float64)
        self.assertIn(df["dividend"].dtype, (np.float64, np.int64))

        if length is not None:
            self.assertAlmostEqual(len(df), length, places=length_places)


class TestYahooFinanceDataGetter(DataGetter):
    def test_simple_get(self):
        """Tests a single get request."""
        dg = data_getter_factory("yfinance")
        df: pd.DataFrame = dg.get_data("IBM", "1m", "1d")
        self.assertValidDataFrame(df)

    def test_get_from_cache_no_compute(self):
        """Tests a second get request fetches the data from cache correctly."""
        dg = data_getter_factory("yfinance")
        df: pd.DataFrame = dg.get_data("IBM", "1m", "1d")
        _df: pd.DataFrame = dg.get_data("IBM", "1m", "1d")
        self.assertEqual(id(_df), id(df))
        self.assertValidDataFrame(_df, length=len(df), length_places=0)

    def test_get_from_cache_compute(self):
        """Tests a second, shorter get request computes the data from cache correctly."""
        dg = data_getter_factory("yfinance")
        df: pd.DataFrame = dg.get_data("IBM", "1d", "1y")
        _df: pd.DataFrame = dg.get_data("IBM", "1mo", "6mo")
        self.assertIsNotNone(_df)
        self.assertNotEqual(id(_df), id(df))
        self.assertValidDataFrame(_df, length=6, length_places=0)

    def test_get_ignore_cache(self):
        """Tests a second, broader get request that the cache cannot compute."""
        dg = data_getter_factory("yfinance")
        df: pd.DataFrame = dg.get_data("IBM", "1d", "1y")
        _df: pd.DataFrame = dg.get_data("IBM", "1mo", "2y")
        self.assertIsNotNone(_df)
        self.assertNotEqual(id(_df), id(df))
        self.assertValidDataFrame(_df, length=24, length_places=0)
