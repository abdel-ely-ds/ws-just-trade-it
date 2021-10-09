from typing import List, Union
from wsgiref.validate import validator

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    GIT_VISION: str = "dev"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "Just TradeIt"
    DESCRIPTION: str = "backtesting api powered by AI"
    ALLOW_ORIGINS: list = ["*"]
    ALLOW_METHODS: list = ["*"]
    ALLOW_HEADERS = ["*"]
    ALLOW_CREDENTIALS: bool = True


settings = Settings()
