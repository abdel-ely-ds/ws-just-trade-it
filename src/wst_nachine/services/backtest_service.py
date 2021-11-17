import os
from typing import Type
from t_nachine.backtester import Backtest, Strategy
import pandas as pd

LOG_FOLDER = "/tmp/logs"
STOCKS_PATH = "stocks/"


class BacktestService:

    def __init__(self) -> None:
        self.bt = Backtest(cash=10_000)

    def run(self,
            strategy: Type[Strategy],
            stock_name: str = "msft.us.txt",
    ) -> dict:
        stock_path = os.path.join(STOCKS_PATH, stock_name)
        results: pd.DataFrame = self.bt.run(strategy=strategy, stock_path=stock_path)
        results.fillna('None', inplace=True)
        return results.to_dict()


