import pandas as pd

class EMA:
    def __init__(self, stock: pd.DataFrame, windows: list[int]):
        self.stock = stock.copy()
        self.windows = windows

    def run(self)-> pd.DataFrame:
        try:
            for window in self.windows:
                self.stock[f'{window}_EMA'] = self.stock['close'].ewm(span=window, adjust=False).mean()
        except KeyError as ke:
            print(f"KeyError: {ke}")
            raise
        
        except Exception as e:
            print(f"Error calculating EMA: {e}")
            raise
        return self.stock