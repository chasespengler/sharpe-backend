"""
A searchable cache for storing historical finance data.

"""
from __future__ import annotations

import json
from typing import Any, Dict, Optional, Tuple, Union

import pandas as pd
from sharpe.analysis.timestring import TimeString
from sharpe.analysis.utils import resample_dataframe_to_period_interval


class SharpeCache:
    def __init__(self) -> None:
        """
        A cache for analysis requests. Cached data does not expire with time, so this should only
        be used with batch requests.

        When possible, the cache will compute the symbol's data from another interval and period.
        For example, daily data over two years can be used to compute weekly data over one year.
        However, the opposite is not true.

        Because of this unidirectional relationship, the cache has a preference for broader data.
        When updating data for an interval, the cache will check if the new data has a longer
        period. If it does, the cache will update. If it does not, the cache will ignore the new
        data.
        For example, if the cache has daily data over two years and a put is made with data over
        one year, the put will be ignored because the one-year data can be easily computed from
        the two-year data.

        The put checker will not look for computability across intervals. Even though weekly data
        can be created from daily data, the cache will store the weekly data.

        Cache is structured like
        ```json
        {
            "<SYMBOL>": {
                "<INTERVAL>": {
                    "period": "<PERIOD>",
                    "data": "<DATA ADAPTER>"
                }
            }
        }
        ```
        """
        self.__cache: Dict[str, Dict[str, Union[str, pd.DataFrame]]] = {}

    def __str__(self) -> str:
        return json.dumps(self.__cache, cls=CacheJSONEncoder)

    def get(self, symbol: str, interval: str, period: str) -> Optional[pd.DataFrame]:
        """Gets the symbol's data for that period or interval. If it does not exist, the cache will
        attempt to compute it from the symbol's other cached data. If it cannot be computed, None
        will be returned.

        If the data is computed, the cache will attempt to update.

        :param symbol:      Symbol or identifier of the data to acquire from the source
        :param interval:    Time interval data should be returned in
        :param period:      Period of time to get data for
        :return:            Symbol's DataFrame for that period and interval. None if it cannot be\
            computed.
        """
        # Get the symbol's cached data by interval
        cached_intervals = self.__cache.get(symbol)

        # If the symbol has no historical data, ignore
        if cached_intervals is None:
            return

        to_compute_from = self._get_cache_to_compute_from(symbol, interval, period)
        if to_compute_from is None:
            return

        cached_interval, cached_period, cached_df = to_compute_from

        if interval == cached_interval and period == cached_period:
            # This data does not need to be computed and cached
            return to_compute_from[2]

        # Create a DataFrame that meets the interval/period requirements
        df = resample_dataframe_to_period_interval(
            cached_df, TimeString(interval), TimeString(period)
        )

        # Cache
        self.put(symbol, interval, period, df)
        return df

    def put(self, symbol: str, interval: str, period: str, df: pd.DataFrame):
        """Puts the given DataFrame into the symbol's cache if it extend's the cache's ability to
        compute requests. If not, the put is ignored.

        :param symbol:      Symbol or identifier of the data to acquire from the source
        :param interval:    Time interval data should be returned in
        :param period:      Period of time to get data for
        :param df:          DataFrame to put
        """
        cached_intervals = self.__cache.get(symbol)
        if cached_intervals is None:
            self.__cache[symbol] = {}
            cached_period = None
        else:
            cached_period = cached_intervals.get(interval)

        # Conditions where cache should be updated
        # 1. Fill cache if empty
        # 2. Prioritize larger data sets so more potential computations are available
        if cached_period is None:
            self.__cache[symbol][interval] = {"period": period, "data": df}
        elif TimeString(period) >= TimeString(cached_period["period"]):
            self.__cache[symbol][interval] = {"period": period, "data": df}

    def _get_cache_to_compute_from(
        self, symbol: str, interval: str, period: str
    ) -> Optional[Tuple[str, str, pd.DataFrame]]:
        """Gets the interval, period, and DataFrame to use for computing the symbol's given
            interval and period.

        :param symbol:      Symbol or identifier of the data to acquire from the source
        :param interval:    Time interval data should be returned in
        :param period:      Period of time to get data for
        :return:            Tuple containing the interval, period, and DataFrame respectively.\
            None if not possible
        """
        ts_interval = TimeString(interval)
        ts_period = TimeString(period)

        cached_intervals = self.__cache.get(symbol, {})
        # Iterable sorted by TimeString
        iterable = sorted(cached_intervals.items(), key=lambda item: item[0])
        for cached_interval, cached_data in iterable:
            # First check for a more granular interval
            if TimeString(cached_interval) > ts_interval:
                # If there is no lesser interval, then the data cannot be computed
                return

            # Next, check for an equal or broader period
            if TimeString(cached_data["period"]) < ts_period:
                # If there is no >= period, then the data from this interval cannot be used
                continue

            # If we make it here, this data can be used to compute for the desired interval
            return cached_interval, cached_data["period"], cached_data["data"]

        # If the cache is empty, return nothing


JSON_ENCODER_STAMP = "__JSON_ENCODER_STAMP__"


class CacheJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (pd.DataFrame, pd.Series)):
            doc = o.to_dict(orient="list")
            doc[JSON_ENCODER_STAMP] = f"pandas.{type(o).__name__}"
            return doc
        elif isinstance(o, TimeString):
            return {JSON_ENCODER_STAMP: "TimeString", "time_string": o.time_string}
        return super().default(o)


class CacheJSONDecoder(json.JSONDecoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, dict):
            needs_replacement = JSON_ENCODER_STAMP in o
            encoder_type = o.pop(JSON_ENCODER_STAMP, None)
            if encoder_type == "pandas.DataFrame":
                return pd.DataFrame(o)
            elif encoder_type == "pandas.Series":
                return pd.Series(o)
            elif encoder_type == "TimeString":
                return TimeString(o["time_string"])
            else:
                if needs_replacement:
                    o[JSON_ENCODER_STAMP] = encoder_type
        return super().default(o)
