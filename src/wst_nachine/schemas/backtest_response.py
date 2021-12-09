from pydantic import BaseModel, Field


class BacktestResponse(BaseModel):
    backtest_results: str = Field(..., description="backtest results")
