class StockNameDoesNotExist(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class AnalysisTypeDoesNotExist(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class StrategyNotImplemented(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
