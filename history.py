# history.py

import MetaTrader5 as mt5
import pandas as pd
import os
import time

# Initialize MetaTrader 5
def initialize_mt5():
    if not mt5.initialize():
        print("MT5 initialization failed")
        return False
    return True

# Download historical data for a given symbol and timeframe from MetaTrader 5
def download_historical_data(symbol, timeframe, num_bars=1):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)
    if rates is None:
        print(f"Failed to get historical data for {symbol}")
        return None
    return pd.DataFrame(rates)

# Continuously fetch and update CSV data every second
def continuously_update_csv(symbol, timeframe, csv_file):
    if not os.path.exists(csv_file):
        # Initialize CSV if not exists
        print(f"Creating new CSV: {csv_file}")
        pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close', 'tick_volume']).to_csv(csv_file, index=False)

    # Continuous update every second
    while True:
        new_data = download_historical_data(symbol, timeframe, num_bars=1)
        if new_data is not None:
            new_data['time'] = pd.to_datetime(new_data['time'], unit='s')
            new_data.to_csv(csv_file, mode='a', header=False, index=False)  # Append new data to the CSV
            print(f"Updated CSV with new data: {new_data.iloc[-1]}")
        
        time.sleep(1)  # Wait for 1 second before fetching new data
