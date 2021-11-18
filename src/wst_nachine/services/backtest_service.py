import os
from typing import Type

import pandas as pd
from t_nachine.backtester import Backtest, Strategy

LOG_FOLDER = "/tmp/logs"
STOCKS_PATH = "stocks/"
SUFFIX_STOCK_NAMES = "us.txt"


class BacktestService:
    def __init__(self) -> None:
        self.bt = Backtest(cash=10_000)

    def run(
        self,
        strategy: Type[Strategy],
        stock_name: str = "msft",
    ) -> dict:
        results: pd.DataFrame = self.bt.run(
            strategy=strategy,
            stock_path=os.path.join(STOCKS_PATH, f"{stock_name}.{SUFFIX_STOCK_NAMES}"),
        )
        results.fillna("None", inplace=True)
        return results.to_dict()
