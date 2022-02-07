import os
from typing import Optional

from pydantic import BaseModel, Field, validator

from wst_nachine.exceptions import StockNameDoesNotExist

STOCKS = "stocks"
SUFFIX_STOCK_NAMES = "us.txt"

STOCKS_PATH = os.path.abspath(STOCKS)


class DataRequest(BaseModel):
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
