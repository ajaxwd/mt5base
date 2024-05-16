import MetaTrader5 as mt5 

class DataProvider():

    def __init__(self) -> None:
        pass

    def get_lastest_closed_bar(self, symbol: str, timeframe: str):
