"""
Data acquisition tool.

"""
from __future__ import annotations

import abc
import logging
from typing import Optional

import pandas as pd
from sharpe.analysis import utils
from sharpe.analysis.analysis.data.cache import SharpeCache
from sharpe.analysis.timestring import TimeString

logger: logging.Logger = logging.getLogger(__name__)


class SourceDataAdapter(abc.ABC):
    @abc.abstractproperty
    def opening_prices(self) -> pd.Series:
        """Retrieves the opening prices for the acquired data. Should align with the timestamps\
        property."""

    @abc.abstractproperty
    def timestamps(self) -> pd.Series:
        """Retrieves the timestamps throughout the period"""

    @abc.abstractproperty
    def dividends(self) -> pd.Series:
        """Retrieves the dividends paid over the period. Should align with the timestamps\
        property."""


class DataGetter(abc.ABC):
    def __init__(self) -> None:
        self.__data_cache: SharpeCache = SharpeCache()

    @abc.abstractclassmethod
    def label(cls) -> str:
        """DataGetter label for factory.

        :return: The implementation's label.
        """

    @abc.abstractmethod
    def get_from_source(self, symbol: str, interval: str, period: str, **kwds) -> SourceDataAdapter:
        """Gets the specified data from the getter's source.

        :param symbol:      Symbol or identifier of the data to acquire from the source
        :param interval:    Time interval data should be returned in
        :param period:      Period of time to get data for
        :return:            An adapter for accessing opening prices and dividends
        """

    def get_data(
        self, symbol: str, interval: str = "1d", period: str = "5y", **kwds
    ) -> pd.DataFrame:
        """Returns the given symbol's data within the time period and using the interval.

        :param symbol:      Symbol or identifier of the data to acquire from the source
        :param interval:    Time interval data should be returned in
        :param period:      Period of time to get data for
        :return:            A time-series DataFrame containing opening price and dividend columns
        """
        data: Optional[SourceDataAdapter]
        df: Optional[pd.DataFrame]

        df = self.__data_cache.get(symbol, interval, period)
        # Cache will return None if the data does not exist and cannot be computed from other
        # cached data
        if df is None:
            # Get adapter
            data = self.get_from_source(symbol, interval, period, **kwds)
            # Represent in DataFrame
            df: pd.DataFrame = pd.DataFrame(
                dict(price=data.opening_prices, dividend=data.dividends), index=data.timestamps
            )
            # Cannot assume the source will produce properly intervaled data. Format before
            # putting to cache
            df = utils.resample_dataframe_to_period_interval(
                df, TimeString(interval), TimeString(period)
            )
            # Update cache
            self.__data_cache.put(symbol, interval, period, df)

        return df
