import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

def load_historical_data(symbol):
    # Connect to MetaTrader 5
    mt5.initialize()

    # Set time frame and date range
    timeframe = mt5.TIMEFRAME_M15  # 15-minute candles
    utc_from = datetime(2023, 1, 1)
    utc_to = datetime.now()

    # Request historical data
    rates = mt5.copy_rates_range(symbol, timeframe, utc_from, utc_to)

    # Convert to DataFrame
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')

    # Shutdown MetaTrader 5 connection
    mt5.shutdown()

    return data
