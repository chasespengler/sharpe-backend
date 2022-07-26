from ._yfinance import YahooFinanceGetter as __YahooFinanceGetter
from .getter import DataGetter


def data_getter_factory(kind: str) -> DataGetter:
    if kind == __YahooFinanceGetter.label():
        return __YahooFinanceGetter()
    else:
        raise ValueError(
            f"'{kind}' DataGetter kind not in \
                {', '.join(subc.label() for subc in DataGetter.__subclasses__())}"
        )
