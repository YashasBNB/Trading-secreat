# indicator.py

import pandas as pd

# Calculate MACD and Signal Line
def calculate_macd(data, short_term=12, long_term=26, signal=9):
    data['EMA12'] = data['close'].ewm(span=short_term, adjust=False).mean()
    data['EMA26'] = data['close'].ewm(span=long_term, adjust=False).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['Signal'] = data['MACD'].ewm(span=signal, adjust=False).mean()
    return data

# Calculate RSI (Relative Strength Index)
def calculate_rsi(data, window=14):
    delta = data['close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

# Calculate Bollinger Bands
def calculate_bollinger_bands(data, window=20, num_std=2):
    data['MA20'] = data['close'].rolling(window=window).mean()
    data['BB_upper'] = data['MA20'] + num_std * data['close'].rolling(window=window).std()
    data['BB_lower'] = data['MA20'] - num_std * data['close'].rolling(window=window).std()
    return data
