from server.scripts.data_loading import load_data_from_db
from server.indicators.RSI import RSI
from server.indicators.EMA import EMA
from server.indicators.SMA import SMA
from server.indicators.BollingerBands import BollingerBands
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

db_data = load_data_from_db("AAPL", "daily")
# stock_sma = SMA(db_data, [9, 20])
# print(stock_sma.run())

# stock_ema = EMA(db_data, [9, 20])
# print(stock_ema.run())

stock_rsi = RSI(db_data, 14)
print(stock_rsi.run())
stock_rsi.plot()

# stock_bb = BollingerBands(db_data, 14)
# print(stock_bb.run())



# stock = get_rsi_function(db_data)

# stock['date'] = pd.to_datetime(stock['date'])
# stock.set_index('date',inplace=True)

# plt.figure(figsize=(12,8))
# ax1 = plt.subplot(211)
# ax1.plot(stock.index, stock['close'],color='lightgray')
# ax1.set_title("Close Price", color='white')

# ax1.grid(True, color ='#555555')
# ax1.set_axisbelow(True)
# ax1.set_facecolor('black')
# ax1.figure.set_facecolor('#121212')
# ax1.tick_params(axis='x', colors='white')
# ax1.tick_params(axis='y', colors='white')

# ax2 = plt.subplot(212, sharex =ax1)
# ax2.plot(stock.index, stock['rsi_14'],color='lightgray')
# ax2.axhline(0, linestyle='--',alpha=0.5, color='white')
# ax2.axhline(30, linestyle='--',alpha=0.5, color='#ff0000')
# ax2.axhline(70, linestyle='--',alpha=0.5, color='#00ff00')

# ax2.set_title("RSI Value")
# ax2.grid(False)
# ax2.set_axisbelow(True)
# ax2.figure.set_facecolor('#121212')
# ax2.tick_params(axis='x', colors='white')
# ax2.tick_params(axis='y', colors='white')

# plt.show()
# mpf.plot(stock, type='candle', style='yahoo')


