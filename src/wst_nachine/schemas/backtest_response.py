from pydantic import BaseModel, Field


class BacktestResponse(BaseModel):
    average_duration: float = Field(..., description="Average exposure time")
    number_of_trades: float = Field(..., description="number of trades")
    win_rate: float = Field(..., description="win rate of the strategy")
    profit_factor: float = Field(..., description="risk to reward")
    return_pct: float = Field(..., description="ROI")
    worst_trade: float = Field(..., description="PnL of the worst trade")
    best_trade: float = Field(..., description="PnL of the best trade")
    win_10_streak: float = Field(..., description="probability of 10 winning streaks")
    lost_10_streak: float = Field(..., description="probability of 10 losing streaks")
