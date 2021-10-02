from typing import Optional

from pydantic import BaseModel


class Request(BaseModel):
    code: str
    analysis_type: Optional[str] = "MACRO"
    stock_name: Optional[str] = "msft"
