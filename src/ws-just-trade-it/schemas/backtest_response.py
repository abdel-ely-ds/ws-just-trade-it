import pandas as pd
from pydantic import BaseModel, Field


class BacktestResponse(BaseModel):
    backtest_results: pd.DataFrame = Field(..., description="backtest results")

    class Config:
        arbitrary_types_allowed = True
