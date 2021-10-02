import os

from ws_just_tradeit.utils.handle_backtest_request import save_to_python_file, load_latest_strategy
import pandas as pd
from tradeit.backtester import BacktestWrapper

LOG_FOLDER = "/tmp/logs"
STOCKS_PATH = "stocks"


def backtest(self, code: str, analysis_type: str, stock_name, plot=False) -> pd.DataFrame:
    # save str code to python file
    save_to_python_file(code)

    # import the latest strategy
    custom_strategy = load_latest_strategy()

    btw = BacktestWrapper(strategy=custom_strategy,
                          analysis_type=analysis_type,
                          log_folder=LOG_FOLDER)

    return btw.run(os.path.join(stock_name), plot=plot)