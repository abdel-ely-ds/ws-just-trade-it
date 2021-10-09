import os
from typing import Type
from abc import ABC

import pandas as pd

# from tradeit.backtester import BacktestWrapper, Strategy

LOG_FOLDER = "/tmp/logs"
STOCKS_PATH = "stocks"


class Strategy(ABC):
    pass


class BacktestService:
    @staticmethod
    def run(
        strategy: Type[Strategy],
        analysis_type: str = "MACRO",
        stock_name: str = "msft",
        plot=False,
    ) -> dict:
        columns = ["1", "2", "3"]
        return pd.DataFrame(columns=columns).to_dict()
