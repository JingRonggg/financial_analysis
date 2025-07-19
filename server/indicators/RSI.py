import pandas as pd
import matplotlib.pyplot as plt

class RSI:
    def __init__(self, stock: pd.DataFrame, window: int = 14):
        self.stock = stock.copy()
        self.window = window
    
    def run(self) -> pd.DataFrame:
        try:
            change = self.stock['close'].diff()
            self.stock['gain'] = change.apply(lambda x: x if x > 0 else 0)
            self.stock['loss'] = change.apply(lambda x: -x if x < 0 else 0)

            self.stock['ema_gain'] = self.stock['gain'].ewm(com=self.window-1, min_periods = self.window).mean()
            self.stock['ema_loss'] = self.stock['loss'].ewm(com=self.window-1, min_periods = self.window).mean()

            self.stock['rs'] = self.stock['ema_gain']/self.stock['ema_loss']
            self.stock[f'rsi_{self.window}'] = 100 - (100/(1 + self.stock['rs']))

            self.stock['overbought'] = self.stock[f'rsi_{self.window}'] > 70
            self.stock['oversold'] = self.stock[f'rsi_{self.window}'] < 30

        except KeyError as e:
            print(f"Key Error: {e}")
            raise

        except Exception as e:
            print(f"Error calculating RSI: {e}")
            raise
        
        return self.stock
    
    def plot(self):
        rsi_col = f'rsi_{self.window}'
        if rsi_col not in self.stock.columns:
            print("RSI not calculated yet. Run run() first.")
            return
        
        plt.figure(figsize=(12, 6))
        plt.plot(self.stock[rsi_col], label=f'RSI {self.window}', color='blue')
        plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
        plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
        plt.title(f'Relative Strength Index (RSI) - {self.window} periods')
        plt.xlabel('Index')
        plt.ylabel('RSI Value')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

