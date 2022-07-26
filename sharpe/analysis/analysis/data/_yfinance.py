"""
Data acquisition framework for yfinance.

"""
from __future__ import annotations

import numpy as np
import pandas as pd
import yfinance
from sharpe.analysis.analysis.data.getter import DataGetter, SourceDataAdapter


class YahooFinanceDataAdapter(SourceDataAdapter):
    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__()
        self.data: pd.DataFrame = data

    @property
    def opening_prices(self) -> pd.Series:
        return self.data["Open"]

    @property
    def timestamps(self) -> pd.Series:
        return self.data.index

    @property
    def dividends(self) -> pd.Series:
        if "Dividends" in self.data.columns:
            return self.data["Dividends"]
        return pd.Series(0.0, index=self.data.index, dtype=np.dtype("float64"))


class YahooFinanceGetter(DataGetter):
    @classmethod
    def label(cls):
        return "yfinance"

    def get_from_source(self, symbol: str, interval: str, period: str, **kwds) -> SourceDataAdapter:
        df = yfinance.download(
            symbol,
            period=period,
            interval=interval,
            actions=True,  # actions=True will fetch dividend data as well
            progress=False,
        )
        return YahooFinanceDataAdapter(df)
