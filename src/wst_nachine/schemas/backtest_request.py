import os
from typing import Optional

from pydantic import BaseModel, Field, validator

from wst_nachine.exceptions import StockNameDoesNotExist

FILE_NAME = "dummy_strategy.py"
STOCKS = "stocks"
SUFFIX_STOCK_NAMES = "us.txt"

DUMMY_STRATEGY_PATH = os.path.abspath(FILE_NAME)  # how to write this better ?
STOCKS_PATH = os.path.abspath(STOCKS)

with open(DUMMY_STRATEGY_PATH, "r") as file:
    STRING_CODE = file.read()


class BacktestRequest(BaseModel):
    strategy_code: str = Field(
        default=STRING_CODE,
        description="Your strategy implementation which should be a sub-class of Strategy",
    )

    stock_name: Optional[str] = Field(
        default="msft", description="The name of the stock to backtest"
    )

    @validator("stock_name")
    def validate_stock_name(cls, v):  # noqa:  B902
        stock_names = os.listdir(STOCKS_PATH)
        if f"{v}.{SUFFIX_STOCK_NAMES}" not in stock_names:
            msg = f"Your stock {v} does not exist in our database"
            raise StockNameDoesNotExist(msg)
        return v
