from fastapi import BackgroundTasks, FastAPI, Request

from ws_just_tradeit.schemas import BacktestRequest, BacktestResponse
from ws_just_tradeit.services import backtest
from ws_just_tradeit.utils.handle_backtest_request import (
    load_latest_strategy,
    save_to_python_file,
)

app = FastAPI()


@app.post("/backtest", response_model=BacktestResponse)
async def backtest_strategy(backtest_request: BacktestRequest):

    # save str code to python file
    save_to_python_file(strategy_code=backtest_request.strategy_code)
    custom_strategy = load_latest_strategy()

    btr = backtest(
        strategy=custom_strategy,
        analysis_type=backtest_request.analysis_type,
        stock_name=backtest_request.stock_name,
    )
    return BacktestResponse(btr)
