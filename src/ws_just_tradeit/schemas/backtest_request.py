from typing import Optional

from pydantic import BaseModel, Field, validator

from .exceptions import AnalysisTypeDoesNotExist, StockNameDoesNotExist

AVAILABLE_ANALYSIS = ["MACRO", "MICRO"]


class BacktestRequest(BaseModel):
    strategy_code: str = Field(
        ...,
        description="Your strategy implementation which should be a sub-class of Strategy",
    )
    analysis_type: Optional[str] = Field(
        default="MACRO", description="Two available types of analysis: MACRO & MICRO"
    )
    stock_name: Optional[str] = Field(
        default="msft", description="The name of the stock to backtest"
    )

    @validator("stock_name")
    def validate_stock_name(cls, v):  # noqa:  B902
        with open("stocks/stocks_names.txt") as f:
            stocks_names = f.readlines()
            if v not in stocks_names:
                msg = f"Your stock {v} does not exist in our database"
                raise StockNameDoesNotExist(msg)

    @validator("analysis_type")
    def validate_analysis_type(cls, v):  # noqa:  B902
        if v not in AVAILABLE_ANALYSIS:
            msg = f"Please provide one of the following Analysis {AVAILABLE_ANALYSIS}"
            raise AnalysisTypeDoesNotExist(msg)
