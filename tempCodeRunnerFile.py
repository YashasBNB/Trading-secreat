import MetaTrader5 as mt5
from ai_trader import ai_trade_decision
import time
from config import MT5_ACCOUNT, MT5_PASSWORD, MT5_SERVER  # Import account details

symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD', 'NZDUSD', 'USDCHF']

def execute_trades():
    if not mt5.initialize():
        print("MetaTrader 5 initialization failed")
        return
    
    if not mt5.login(MT5_ACCOUNT, MT5_PASSWORD, server=MT5_SERVER):
        print("Login failed")
        return
    
    print("Connected to MetaTrader 5")

    for symbol in symbols:
        decision = ai_trade_decision(symbol)
        
        if decision == "buy":
            print(f"Buying {symbol}")
            # Add buy trade logic here
        elif decision == "sell":
            print(f"Selling {symbol}")
            # Add sell trade logic here
        else:
            print(f"Hold position for {symbol}")

    mt5.shutdown()  # It's a good practice to shut down the connection after trades

if __name__ == "__main__":
    while True:
        execute_trades()
        time.sleep(180)  # 3 minutes
