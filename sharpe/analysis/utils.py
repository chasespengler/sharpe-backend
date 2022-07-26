"""


"""
from __future__ import annotations

import functools
import logging
import traceback
from typing import TYPE_CHECKING, Any, Tuple, Union

import pandas as pd

if TYPE_CHECKING:
    from sharpe.analysis.timestring import TimeString

null_logger: logging.Logger = logging.Logger("null")


def resample_dataframe_to_period_interval(
    df: pd.DataFrame, interval: TimeString, period: TimeString
) -> pd.DataFrame:
    """Resamples a DataFrame to the specified interval and period. Uses the mean for each group.

    :param df:          Time-series DataFrame to resample
    :param interval:    Time interval data should be returned in
    :param period:      Period of time to get data for
    :return:            A time-series DataFrame averaged to use the specified interval and\
        period.
    """
    rdf: pd.DataFrame = df.copy()
    rdf: pd.DataFrame = rdf.resample(
        rule=interval.pandas_offset_alias(prepend_value=True),
        kind="period",
    ).agg({"price": "mean", "dividend": "sum"})
    rdf.set_index(rdf.index.to_timestamp(), inplace=True)
    dt = period.period_start()
    rdf.drop(rdf[rdf.index <= dt].index, inplace=True)
    return rdf


def retry(
    max_retry: int,
    exception: Union[BaseException, Tuple[BaseException]] = BaseException,
    logger: logging.Logger = null_logger,
):
    """Returns a decorator for retrying a function's execution a set number of times after errors.
    Will catch specific exceptions and log them.

    :param max_retry:   Maximum number of retries (not including original attempt)
    :param exception:   Exception(s) to catch. Will raise if `max_retry` is surpassed, defaults to\
                        `BaseException`
    :param logger:      Logger to report errors and retries with, defaults to null_logger
    :return:            A decorator for wrapping the function to be retried.
    :raises:            Any
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwds) -> Any:
            attempts = 0
            while True:
                try:
                    return func(*args, **kwds)
                except exception as e:
                    e: BaseException
                    # incrementing here for logging purposes (attempt # more obvious than retry #)
                    # use <= max_retry since attempt=1 == retry=0, attempt=2 == retry=1, ...
                    attempts += 1
                    if attempts <= max_retry:
                        # Retry available, log and move on
                        logger.debug(
                            "Retryable error after %(attempt)s attempt caught after calling\
                                %(wrapped_func_name)s",
                            extra=dict(
                                wrapped_func_name=func.__name__,
                                attempt=attempts,
                                error=traceback.format_exc(),
                            ),
                        )
                    else:
                        # retry unavailable, log and raise
                        logger.error(
                            "Non-retryable error after %(attempt)s attempt caught after calling\
                                 %(wrapped_func_name)s",
                            extra=dict(
                                wrapped_func_name=func.__name__,
                                attempt=attempts,
                                error=traceback.format_exc(),
                            ),
                        )
                        raise e

        return wrapper

    return decorator
