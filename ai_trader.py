# ai_trader.py
from news_fetcher import fetch_news, analyze_sentiment
from market_data import fetch_market_data, calculate_moving_average
import MetaTrader5 as mt5

def ai_trade_decision(symbol="EURUSD"):
    # Fetch market data
    rates = fetch_market_data(symbol=symbol)
    
    # Calculate moving average
    moving_avg = calculate_moving_average(rates)
    last_close = rates[-1]['close']
    
    # Fetch and analyze news sentiment
    news_data, _ = fetch_news()
    sentiment = analyze_sentiment(news_data)
    
    # Decision: Buy/Sell based on news sentiment and moving average
    if sentiment == "bullish" and last_close > moving_avg:
        return "buy"
    elif sentiment == "bearish" and last_close < moving_avg:
        return "sell"
    else:
        return "hold"

def place_trade(symbol="EURUSD", action="buy", lot=0.1):
    trade_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(symbol).ask,
        "deviation": 20,
        "magic": 234000,
        "comment": "AI-based trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(trade_request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Failed to place {action} trade, retcode: {result.retcode}")
    else:
        print(f"Trade successful: {action}, {result}")
