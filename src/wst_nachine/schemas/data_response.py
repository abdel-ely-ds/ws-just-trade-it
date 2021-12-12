from pydantic import BaseModel, Field


class DataResponse(BaseModel):
    data: str = Field(..., description="stock data")
