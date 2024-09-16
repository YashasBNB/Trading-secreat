# main.py
import time
from metatrade import initialize_mt5
from ai_trader import ai_trade_decision, place_trade

if __name__ == "__main__":
    if initialize_mt5():
        print("Connected to MetaTrader 5")
        
        symbol = "EURUSD"
        while True:
            decision = ai_trade_decision(symbol=symbol)
            if decision in ["buy", "sell"]:
                place_trade(symbol=symbol, action=decision)
            else:
                print("Hold position")
            
            # Wait for 1 minute before the next decision
            time.sleep(180)