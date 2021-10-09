import glob
import importlib
import os
from typing import Type
from ws_just_tradeit.exceptions.exceptions import StrategyNotImplemented
from ws_just_tradeit.services.backtest_service import Strategy
from pathlib import Path

CUSTOM_STRATEGIES_FOLDER = r"custom_strategies"
HOME = r"C:\Users\abdel\Desktop\Workspace\ws-just-trade-it\src\ws_just_tradeit"
SRC = "ws_just_tradeit"


def create_custom_strategies_package():
    Path(f"{HOME}/{CUSTOM_STRATEGIES_FOLDER}/").mkdir(parents=True, exist_ok=True)
    with open(os.path.join(CUSTOM_STRATEGIES_FOLDER, "__init__.py"), "w") as f:
        f.write("")


def get_latest_strategy() -> Type[Strategy]:
    strategy_name = Path(get_latest_added_file()).parts[-1].split(".")[0]
    module_name = f"{SRC}.{CUSTOM_STRATEGIES_FOLDER}.{strategy_name}"
    try:
        return getattr(importlib.import_module(module_name), strategy_name)()

    except AttributeError:
        raise StrategyNotImplemented


def save_to_python_file(strategy_code: str) -> None:
    create_custom_strategies_package()
    strategy_name = strategy_code[: strategy_code.index("(Strategy)")].split(" ")[-1]
    with open(os.path.join(CUSTOM_STRATEGIES_FOLDER, strategy_name + ".py"), "w") as f:
        f.write(strategy_code)


def get_latest_added_file() -> str:
    list_of_files = glob.glob(f"{HOME}/{CUSTOM_STRATEGIES_FOLDER}/*.py")
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file
