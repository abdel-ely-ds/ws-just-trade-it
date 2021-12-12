from pydantic import BaseModel, Field


class BacktestResponse(BaseModel):
    first_trade: str = Field(..., description="date of first trade")
    last_trade: str = Field(..., description="date of last trade")
    exposure_time: str = Field(..., description="Average exposure time")
    nb_trades: float = Field(..., description="number of trades")
    win_rate: float = Field(..., description="win rate of the strategy")
    profit_factor: float = Field(..., description="risk to reward")
    pct_return: float = Field(..., description="ROI")
    worst_trade: float = Field(..., description="PnL of the worst trade")
    best_trade: float = Field(..., description="PnL of the best trade")
    win_10_streak: float = Field(..., description="probability of 10 winning streaks")
    lost_10_streak: float = Field(..., description="probability of 10 losing streaks")
