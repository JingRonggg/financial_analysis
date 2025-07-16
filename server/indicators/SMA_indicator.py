def get_SMA(stock, slow_period, fast_period):
    try:
        stock[f'{fast_period}_SMA'] = stock['close'].rolling(window=fast_period).mean()
        stock[f'{slow_period}_SMA'] = stock['close'].rolling(window=slow_period).mean()
    except Exception as e:
        print(f"Error calculating SMA: {e}")
        raise

    return stock