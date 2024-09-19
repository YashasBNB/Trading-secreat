import pandas as pd
import MetaTrader5 as mt5

# Fetch data from CSV
def fetch_csv_data(pair, timeframe):
    try:
        data = pd.read_csv(f'{pair}_{timeframe}_data.csv')
        return data
    except FileNotFoundError:
        print(f"Error: {pair}_{timeframe}_data.csv not found.")
        return None

# Fetch data from MetaTrader 5
def fetch_mt5_data(pair, timeframe, num_bars=500):
    if not mt5.initialize():
        print("Failed to initialize MetaTrader5")
        return None

    timeframe_mapping = {
        '1m': mt5.TIMEFRAME_M1,
        '5m': mt5.TIMEFRAME_M5,
        '15m': mt5.TIMEFRAME_M15
    }

    rates = mt5.copy_rates_from(pair, timeframe_mapping[timeframe], num_bars)
    data = pd.DataFrame(rates)
    data['timestamp'] = pd.to_datetime(data['time'], unit='s')
    return data

# Decide data source: CSV or MetaTrader 5
def fetch_data(pair, timeframe, source='csv'):
    if source == 'csv':
        return fetch_csv_data(pair, timeframe)
    elif source == 'mt5':
        return fetch_mt5_data(pair, timeframe)
    else:
        print("Invalid data source")
        return None
