# market_data.py
import MetaTrader5 as mt5
from datetime import datetime

def fetch_market_data(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M1, bars=100):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    return rates

def calculate_moving_average(rates, period=10):
    closing_prices = [rate['close'] for rate in rates]
    moving_avg = sum(closing_prices[-period:]) / period
    return moving_avg