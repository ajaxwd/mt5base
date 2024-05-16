from platform_connector.platform_connector import PlatformConnector

if __name__ == "__main__":

    symbols = ['EURUSD', 'USDJPY']
    
    CONNECT = PlatformConnector(symbols_list=symbols)