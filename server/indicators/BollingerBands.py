import pandas as pd

class BollingerBands:
    def __init__(self, stock: pd.DataFrame, window: int = 20):
         self.stock = stock.copy()
         self.window = window
         
    def run(self)-> pd.DataFrame:
        try:
            ma_column = f'{self.window}_MA'
            std = self.stock['close'].rolling(window=self.window).std()

            self.stock[ma_column] = self.stock['close'].rolling(window=self.window).mean()
            self.stock['upper'] = self.stock[ma_column] + 2 * std
            self.stock['lower'] = self.stock[ma_column] - 2 * std
            
        except KeyError as ke:
            print(f"KeyError: {ke}")
            raise
        
        except Exception as e:
            print(f"Error calculating Bollinger Bands: {e}")
            raise

        return self.stock
