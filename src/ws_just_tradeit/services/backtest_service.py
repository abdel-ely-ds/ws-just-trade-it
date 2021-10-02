import os
from typing import Type

import pandas as pd
from tradeit.backtester import BacktestWrapper, Strategy

LOG_FOLDER = "/tmp/logs"
STOCKS_PATH = "stocks"


def backtest(
    strategy: Type[Strategy], analysis_type: str, stock_name, plot=False
) -> pd.DataFrame:

    btw = BacktestWrapper(
        strategy=strategy, analysis_type=analysis_type, log_folder=LOG_FOLDER
    )

    return btw.run(os.path.join(STOCK_PATH, stock_name), plot=plot)
