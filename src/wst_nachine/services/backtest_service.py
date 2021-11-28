import os
from typing import Type, List

import pandas as pd
from t_nachine.backtester import Backtest, Strategy

LOG_FOLDER = "/tmp/logs"
STOCKS_PATH = "stocks/"
SUFFIX_STOCK_NAMES = "us.txt"
COLUMNS_TO_RETURN = [
    "Symbol",
    "Size",
    "SlPrice",
    "TpPrice",
    "EntryPrice",
    "ExitPrice",
    "PnL",
    "EntryTime",
    "ExitTime",
]


class BacktestService:
    def __init__(self) -> None:
        self.bt = Backtest(cash=10_000)

    def run(
        self,
        strategy: Type[Strategy],
        stock_name: str = "msft",
        columns_to_return: List[str] = None,
    ) -> dict:
        if columns_to_return is None:
            columns_to_return = COLUMNS_TO_RETURN
        results: pd.DataFrame = self.bt.run(
            strategy=strategy,
            stock_path=os.path.join(STOCKS_PATH, f"{stock_name}.{SUFFIX_STOCK_NAMES}"),
        )
        results.fillna("None", inplace=True)
        results = results[columns_to_return]
        return results.to_dict()
