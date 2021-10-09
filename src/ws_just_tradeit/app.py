import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from ws_just_tradeit.schemas import BacktestRequest, BacktestResponse
from ws_just_tradeit.services.backtest_service import BacktestService
from ws_just_tradeit.utils.handle_backtest_request import (
    get_latest_strategy,
    save_to_python_file,
)

from starlette.requests import Request as StarletteRequest

from ws_just_tradeit.core.settings import settings

from fastapi.middleware.cors import CORSMiddleware

backtest_service = BacktestService()

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


@app.post("/backtest", response_model=BacktestResponse, status_code=200)
async def backtest(backtest_request: BacktestRequest) -> BacktestResponse:
    save_to_python_file(strategy_code=backtest_request.strategy_code)
    custom_strategy = get_latest_strategy()

    return BacktestResponse.parse_obj(
        {
            "backtest_results": backtest_service.run(
                strategy=custom_strategy,
                analysis_type=backtest_request.analysis_type,
                stock_name=backtest_request.stock_name,
            )
        }
    )
