import glob
import importlib
import os
from typing import Type

from wst_nachine.exceptions.exceptions import StrategyNotImplemented
from pathlib import Path
from t_nachine.backtester import Strategy

CUSTOM_STRATEGIES_FOLDER = r"custom_strategies"
HOME = "."


def create_custom_strategies_directory() -> None:
    """
    Create a directory where to save clients strategies
    """
    Path(f"{HOME}/{CUSTOM_STRATEGIES_FOLDER}/").mkdir(parents=True, exist_ok=True)


def get_latest_strategy() -> Type[Strategy]:
    """
    Dynamically import the latest strategy
    """
    strategy_name = Path(get_latest_added_file()).parts[-1].split(".")[0]
    module_name = f"{CUSTOM_STRATEGIES_FOLDER}.{strategy_name}"
    try:
        return getattr(importlib.import_module(module_name), strategy_name)

    except AttributeError:
        raise StrategyNotImplemented


def save_to_python_file(strategy_code: str) -> None:
    """
    It saves the posted strategy code in a custom strategy folder
    """
    create_custom_strategies_directory()
    try:
        key_word = "(Strategy)"
        strategy_name = strategy_code[: strategy_code.index(key_word)].split(" ")[-1]
        with open(os.path.join(CUSTOM_STRATEGIES_FOLDER, strategy_name + ".py"), "w") as f:
            f.write(strategy_code)
    except ValueError:
        raise ValueError("Could not find the the strategy")


def get_latest_added_file() -> str:
    """
    get the latest py file added to the custom strategy folder
    """
    list_of_files = glob.glob(f"{HOME}/{CUSTOM_STRATEGIES_FOLDER}/*.py")
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file
