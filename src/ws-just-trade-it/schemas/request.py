from typing import Optional

from pydantic import BaseModel, Field
from pydantic.typing import DictStrAny


class Request(BaseModel):
    code: str = Field(..., description="Your startegy implementation which should be a sub-class of Strategy")
    analysis_type: Optional[str] = Field(
        default="MACRO", description="Two availble types of analysis: MACRO & MICRO")
    stock_name: Optional[str] = Field(
        default="msft", description="The name of the stock to backtest")
