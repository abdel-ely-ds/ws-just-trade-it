import os
import pandas as pd

STOCKS_PATH = "stocks/"
SUFFIX_STOCK_NAMES = "us.txt"


class DataService:
    stock_path: str = STOCKS_PATH
    suffix_stock_names: str = SUFFIX_STOCK_NAMES

    def get_data(self, stock_name: str):
        df = pd.read_csv(os.path.join(self.stock_path, f"{stock_name}.{self.suffix_stock_names}"))
        return df.to_json(orient="records")
