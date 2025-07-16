import pandas as pd

def get_rsi_function(stock, period = 14, overbought_lvl = 70, oversold_lvl = 30):
    try:
        change = stock['close'].diff()
        stock['gain'] = change.apply(lambda x: x if x > 0 else 0)
        stock['loss'] = change.apply(lambda x: -x if x < 0 else 0)

        stock['ema_gain'] = stock['gain'].ewm(com=period-1, min_periods = period).mean()
        stock['ema_loss'] = stock['loss'].ewm(com=period-1, min_periods = period).mean()

        stock['rs'] = stock['ema_gain']/stock['ema_loss']
        stock[f'rsi_{period}'] = 100 - (100/(1 + stock['rs']))

        return stock
    except Exception as e:
        print(f"Error calculating RSI: {e}")


