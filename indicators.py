import pandas as pd

# RSI calculation
def calculate_rsi(data, period=14):
    delta = data['close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

# MACD calculation
def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    short_ema = data['close'].ewm(span=short_period, adjust=False).mean()
    long_ema = data['close'].ewm(span=long_period, adjust=False).mean()

    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    macd_diff = macd - signal

    return macd, macd_diff

# Calculate indicators
def calculate_indicators(data):
    data['RSI'] = calculate_rsi(data)
    data['MACD'], data['MACD_diff'] = calculate_macd(data)
    
    return data[['RSI', 'MACD_diff']]
