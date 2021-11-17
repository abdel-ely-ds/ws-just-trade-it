import os
from pydantic import BaseModel, Field, validator

from wst_nachine.exceptions import StockNameDoesNotExist

HOME = "/home/abdelelyds/Workspace/PythonProjects/ws-just-trade-it/src/wst_nachine" # how to write this better ?
STOCKS_PATH = "stocks/"
FILE_NAME = "dummy_strategy.py"


with open(os.path.join(HOME, FILE_NAME), "r") as file:
    STRING_CODE = file.read()


class BacktestRequest(BaseModel):
    strategy_code: str = Field(
        default=STRING_CODE,
        description="Your strategy implementation which should be a sub-class of Strategy",
    )

    stock_name: str = Field(
        default="msft.us.txt",
        description="The name of the stock to backtest"
    )

    @validator("stock_name")
    def validate_stock_name(cls, v):  # noqa:  B902
        stock_names = os.listdir(os.path.join(HOME, STOCKS_PATH))
        if v not in stock_names:
            msg = f"Your stock {v} does not exist in our database"
            raise StockNameDoesNotExist(msg)
