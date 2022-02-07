import os
import subprocess

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from starlette.requests import Request as StarletteRequest

from wst_nachine.core.settings import settings
from wst_nachine.schemas import BacktestRequest, BacktestResponse
from wst_nachine.schemas.data_request import DataRequest
from wst_nachine.schemas.data_response import DataResponse
from wst_nachine.services.backtest_service import BacktestService
from wst_nachine.services.data_service import DataService
from wst_nachine.utils.handle_backtest_request import (
    get_latest_strategy,
    save_to_python_file,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.GIT_VISION,
)


@app.on_event("startup")
async def startup_event():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )


@app.get("/", response_class=HTMLResponse, status_code=200)
def index(request: StarletteRequest) -> str:
    return f"""
        <html>
            <head>
                <title>{settings.PROJECT_NAME}</title>
            </head>
            
            <body>
                <h1>{settings.DESCRIPTION}</h1>
                <p>Find documentation  
                    <a href="{os.path.join(request.url.__str__(), "docs")}"> here </a>
                </p>
            </body>
        </html>
        """


@app.post("/backtest_in_docker", response_model=BacktestResponse, status_code=200)
async def run(
        backtest_request: BacktestRequest, backtester: BacktestService = Depends()
) -> BacktestResponse:
    save_to_python_file(strategy_code=backtest_request.strategy_code)
    return BacktestResponse.parse_obj(
        backtester.run(
            strategy=get_latest_strategy(),
            stock_name=backtest_request.stock_name,
        )
    )


@app.post("/backtest", response_model=BacktestResponse, status_code=200)
async def run(
        backtest_request: BacktestRequest, backtester: BacktestService = Depends()
) -> BacktestResponse:
    save_to_python_file(strategy_code=backtest_request.strategy_code)
    return BacktestResponse.parse_obj(
        backtester.run(
            strategy=get_latest_strategy(),
            stock_name=backtest_request.stock_name,
        )
    )


@app.post("/get_data", response_model=DataResponse, status_code=200)
async def get_data(
        data_request: DataRequest, data_service: DataService = Depends()
) -> DataResponse:
    return DataResponse.parse_obj(
        {
            "data": data_service.get_data(
                stock_name=data_request.stock_name,
            )
        }
    )
