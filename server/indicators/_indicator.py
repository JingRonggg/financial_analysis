import pandas as pd

def get_EMA(stock, slow_period, fast_period):
    try:
        stock[f'{slow_period}_EMA'] = stock['close'].ewm(span=slow_period, adjust=False).mean()
        stock[f'{fast_period}_EMA'] = stock['close'].ewm(span=fast_period, adjust=False).mean()
    except Exception as e:
        print(f"Error calculating EMA: {e}")
        raise
    return stock