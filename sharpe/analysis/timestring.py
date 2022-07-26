"""
A class for performing operations on yfinance interval/period time strings.

"""
from __future__ import annotations

import re
from datetime import datetime, tzinfo
from typing import Optional, Tuple

from dateutil.relativedelta import relativedelta

# Ascending order for comparison purposes
TIMESTRINGS = (
    "1m",
    "2m",
    "5m",
    "15m",
    "30m",
    "60m",
    "1h",
    "90m",
    "1d",
    "5d",
    "1wk",
    "1mo",
    "3mo",
    "6mo",
    "1y",
    "2y",
    "5y",
    "10y",
)

# These align with Pandas's offset alias symbols
# https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
TIMESTRING_PANDAS_OFFSET_ALIAS_MAPPER = {
    "m": "T",
    "h": "H",
    "d": "D",
    "wk": "W",
    "mo": "M",
    "y": "Y",
}

# These align with dateutil.relativedelta.relativedelta's keyword arguments
TIMESTRING_RELATIVEDELTA_MAPPER = {
    "m": "minutes",
    "h": "hours",
    "d": "days",
    "wk": "weeks",
    "mo": "months",
    "y": "years",
}

# Cannot make assumptions beyond 'week' unit due to varying days in a month & year
TIMESTRING_TO_MINUTES = {"m": 1, "h": 60, "d": 1440, "wk": 10080}

# Cannot make assumptions before 'month' unit due to varying days in a month & year
TIMESTRING_TO_MONTHS = {"mo": 1, "y": 1 / 12}

# These align with Alpha Vantage's interval symbols
# Note that these only apply to intraday data. For example, there is no 3 month or 6 month
# interval. Alpha Vantage's other intervals are encapsulated in their own APIs (e.g. daily, weekly)
# https://www.alphavantage.co/documentation/#intraday
TIMESTRING_ALPHAVANTAGE_INTERVAL_MAPPER = {
    "1m": "1min",
    "5m": "5min",
    "15m": "15min",
    "30m": "30min",
    "60m": "60min",
    "1h": "60min",
}

# These align with Alpha Vantage's period symbols
# https://www.alphavantage.co/documentation/#intraday
TIMESTRING_ALPHAVANTAGE_SLICE_MAPPER = {}


class TimeString:

    __slots__ = ["time_string"]
    __rgx: re.Pattern = re.compile(r"^(\d+)([a-z]{1,2})$")

    def __init__(self, time_string: str) -> None:
        """Wrapper for time strings used by the yfinance library. Time strings are applicable for
        intervals and periods.

        :param time_string: yfinance time string

        Supported time strings include

            1m, 2m, 5m, 15m, 30m, 60m, 1h, 90m, 1d, 5d, 1wk, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y

        """
        self.time_string: str = time_string

    def unit_value(self) -> Tuple[str, int]:
        """Parses the unit and integer value from the time string.

        ```py
        >>> TimeString("1m").unit_value()
        'm', 1
        ```

        :raises ValueError: TimeString does not match `^(\\d+)([a-z]{1,2})$`
        :return:            The unit and integer value, respectively
        """
        try:
            value, unit = self.__rgx.match(self.time_string).groups()
            return unit, int(value)
        except AttributeError as e:
            # Caused by:
            #  - Pattern does not match (numbers followed by 1-2 lowercase letters), regex returns
            #    None instead of Match with groups method.
            raise ValueError(
                f"Unable to parse timestring unit and value from {repr(self)}: {str(e)}"
            )

    @property
    def unit(self) -> str:
        return self.unit_value()[0]

    @property
    def value(self) -> int:
        return self.unit_value()[1]

    def pandas_offset_alias(self, prepend_value: bool = False) -> str:
        """Convert the TimeString's string representation to a frequency string supported by
        Pandas.

        :param prepend_value:   Prepend the time string's value to the offset alias (e.g. 3T as\
            opposed to T)
        :raises KeyError:       TimeString's unit code is not supported
        :return:                Pandas-recognizable frequency string
        """
        try:
            unit, value = self.unit_value()
            _unit = TIMESTRING_PANDAS_OFFSET_ALIAS_MAPPER[unit]
            return f"{value}{_unit}" if prepend_value else _unit
        except KeyError as e:
            # Caused by:
            #  - Extracted unit is not supported
            raise KeyError(
                f"Failed to convert {repr(self)} offset alias: {e.args[0]} not in\
                {','.join(TIMESTRING_PANDAS_OFFSET_ALIAS_MAPPER)}"
            )

    @property
    def alphavantage_interval(self) -> Optional[str]:
        """Gets the interval used by the Alpha Vantage API, if available.

        :return: Alpha Vantage interval string if available, None otherwise
        """
        return TIMESTRING_ALPHAVANTAGE_INTERVAL_MAPPER.get(self.time_string)

    def period_start(self, tz: Optional[tzinfo] = None) -> datetime:
        """Returns the datetime of the TimeString relative to now.

        :param tz:          Time zone to use for `datetime.now`, defaults to datetime.tzinfo
        :raises KeyError:   TimeString's unit code is not supported
        :raises ValueError: TimeString does not match `^(\\d+)([a-z]{1,2})$`
        :return:            Starting datetime of the TimeString relative to now

        e.g. '1y' should return the datetime for exactly one year ago from now.

        """
        try:
            unit, value = self.unit_value()
            dt = datetime.now(tz=tz)
            td = relativedelta(**{TIMESTRING_RELATIVEDELTA_MAPPER[unit]: value})
            return dt - td
        except KeyError as e:
            # Caused by:
            #  - Extracted unit is not supported
            raise KeyError(
                f"Failed to convert {repr(self)} period start: {e.args[0]} not in\
                {','.join(TIMESTRING_RELATIVEDELTA_MAPPER)}"
            )
        # Note:
        #  - TypeError not needed because pattern will not match unless starting characters
        #    are numbers

    def __hash__(self) -> int:
        return hash(self.time_string)

    def __repr__(self) -> str:
        return f"TimeString('{self.time_string}')"

    def __str__(self) -> str:
        return self.time_string

    def __eq__(self, b: TimeString) -> bool:
        return self.time_string == b.time_string

    def __ne__(self, b: TimeString) -> bool:
        return self.time_string != b.time_string

    def __lt__(self, b: TimeString) -> bool:
        return TIMESTRINGS.index(self.time_string) < TIMESTRINGS.index(b.time_string)

    def __le__(self, b: TimeString) -> bool:
        return TIMESTRINGS.index(self.time_string) <= TIMESTRINGS.index(b.time_string)

    def __gt__(self, b: TimeString) -> bool:
        return TIMESTRINGS.index(self.time_string) > TIMESTRINGS.index(b.time_string)

    def __ge__(self, b: TimeString) -> bool:
        return TIMESTRINGS.index(self.time_string) >= TIMESTRINGS.index(b.time_string)
