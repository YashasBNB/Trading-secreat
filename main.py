# main.py

import pandas as pd
import time
import MetaTrader5 as mt5
import matplotlib.pyplot as plt
from threading import Thread
from history import initialize_mt5, continuously_update_csv
from indicators import calculate_macd, calculate_rsi, calculate_bollinger_bands
from trade_decision import create_features_and_labels, train_ml_model, make_ml_trade_decision

# Live chart plot
def live_chart(symbol, timeframe, csv_file):
    plt.ion()  # Enable interactive mode for live updating chart
    fig, ax = plt.subplots()

    while True:
        data = pd.read_csv(csv_file)
        data['time'] = pd.to_datetime(data['time'], unit='s', errors='coerce')  # Correct time parsing

        # Clear the plot and replot
        ax.clear()
        ax.plot(data['time'], data['close'], label="Close Price")
        ax.set_title(f'Live Chart: {symbol}')
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        ax.legend()

        # Refresh the plot every second
        plt.pause(1)

# Monitor data and make trade decisions
def monitor_and_trade(symbol, timeframe, csv_file):
    model = None
    while True:
        data = pd.read_csv(csv_file)

        # Convert the 'time' column to a proper datetime object, handle bad timestamps
        data['time'] = pd.to_datetime(data['time'], unit='s', errors='coerce')

        # Drop rows where 'time' conversion failed
        data = data.dropna(subset=['time'])

        # Calculate technical indicators
        data = calculate_macd(data)
        data = calculate_rsi(data)
        data = calculate_bollinger_bands(data)

        # Create features and labels for ML
        data = create_features_and_labels(data)

        if model is None:
            # Train ML model only once at the start
            model = train_ml_model(data)

        # Make a trade decision based on the latest data
        decision = make_ml_trade_decision(model, data)
        print(f"AI-based decision for {symbol} on timeframe {timeframe}: {decision}")

        # Notify the user if there's a buy/sell decision
        if decision == "BUY" or decision == "SELL":
            print(f"TRADE ALERT: {decision} on {symbol}!")

        time.sleep(1)  # Check every second

def main():
    if not initialize_mt5():
        return

    symbol = "EURUSD"
    timeframe = mt5.TIMEFRAME_M1
    csv_file = f"{symbol}_{timeframe}_data.csv"

    # Start updating CSV data every second
    continuously_update_csv_thread = Thread(target=continuously_update_csv, args=(symbol, timeframe, csv_file))
    continuously_update_csv_thread.daemon = True
    continuously_update_csv_thread.start()

    # Start the live chart visualization
    live_chart_thread = Thread(target=live_chart, args=(symbol, timeframe, csv_file))
    live_chart_thread.daemon = True
    live_chart_thread.start()

    # Monitor the data and make trade decisions
    monitor_and_trade(symbol, timeframe, csv_file)

    mt5.shutdown()

if __name__ == "__main__":
    main()
