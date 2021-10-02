import glob
import os
import importlib
from typing import Type
from tradeit import Strategy


def load_latest_strategy(python_filepath) -> Type[Strategy]:
    strategy_name = get_latest_added_file()
    python_module = importlib.import_module(python_filepath)
    try:
        return getattr(python_module, strategy_name)()

    except AttributeError:
        return None


def save_to_python_file(strategy_code: str) -> None:
    strategy_name = strategy_code[:strategy_code.index("[Strategy]")].split(" ")[-1]
    with open(f"/custom_strategies/{strategy_name}.py", "w") as f:
        f.write(strategy_code)


def get_latest_added_file() -> str:
    list_of_files = glob.glob('/custom_strategies/*.py')
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file
