from pydantic import BaseModel, Field


class BacktestResponse(BaseModel):
    backtest_results: dict = Field(..., description="backtest results")
