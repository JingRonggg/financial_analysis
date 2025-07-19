import pandas as pd

class SMA:
    def __init__(self, stock: pd.DataFrame, windows: list[int])-> None:
        self.stock = stock.copy()
        self.windows = windows
    
    def run(self) -> pd.DataFrame:
        try:
            for window in self.windows:
                self.stock[f'{window}_SMA'] = self.stock['close'].rolling(window=window).mean()
                
        except KeyError as ke:
            print(f"KeyError: {ke}")
            raise
        
        except Exception as e:
            print(f"Error calculating SMA: {e}")
            raise

        return self.stock