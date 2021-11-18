import os
from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    GIT_VISION: str = "dev"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "T-Nachine"
    DESCRIPTION: str = "backtesting api powered by AI"
    ALLOW_ORIGINS: list = ["*"]
    ALLOW_METHODS: list = ["*"]
    ALLOW_HEADERS = ["*"]
    ALLOW_CREDENTIALS: bool = True

    HOME: str = os.getcwd()


settings = Settings()
