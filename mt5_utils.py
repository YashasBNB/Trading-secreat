import MetaTrader5 as mt5
from config import MT5_ACCOUNT, MT5_PASSWORD, MT5_SERVER

def initialize_mt5():
    if not mt5.initialize():
        print("MetaTrader 5 initialization failed")
        return False
    if not mt5.login(MT5_ACCOUNT, MT5_PASSWORD, server=MT5_SERVER):
        print("Login failed")
        mt5.shutdown()
        return False
    return True
