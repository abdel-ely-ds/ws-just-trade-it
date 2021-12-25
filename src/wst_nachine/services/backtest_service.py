import os
from typing import Type, List

import pandas as pd
from t_nachine.backtester import Backtest, Strategy
from t_nachine.optimization import Analyzer

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
        results = results
        analyzer = Analyzer(results)

        return {
            "average_duration": analyzer.average_exposure_time,
            "number_of_trades": analyzer.nb_trades,
            "win_rate": analyzer.win_rate,
            "profit_factor": analyzer.profit_factor,
            "return_pct": analyzer.pct_return,
            "worst_trade": analyzer.worst_trade,
            "best_trade": analyzer.best_trade,
            "win_10_streak": analyzer.winning_streak_probability(),
            "lost_10_streak": analyzer.losing_streak_probability(),
        }
