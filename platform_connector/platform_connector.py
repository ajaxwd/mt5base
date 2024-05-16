import MetaTrader5 as mt5
import os
from dotenv import load_dotenv, find_dotenv

class PlatformConnector():

    def __init__(self, symbols_list: list) -> None:
        
        # Buscamos el archivo .env y cargamos sus valores
        load_dotenv(find_dotenv())

        # Inicializacion de la plataforma
        self._initialize_platform()

        # Comprobacion del tipo de cuenta
        self._live_account_warning()

        # Imprimimos informacion de la cuenta
        self._print_account_info()

        # Comprobacion del trading algoritmico
        self._check_algo_tradin_enable()

        # Añadir los simbolos al MarketWatch
        self._add_symbols_to_maretwatch(symbols_list)

        

    def _initialize_platform(self) -> None:
        """
        inicializacion de la plataforma de MT5

        Raises:
                Exception: Mandamos un error cuando inicializamos la plataforma

        Returns:
                None
        """
        if mt5.initialize(
            path=os.getenv("MT5_PATH"),
            login=int(os.getenv("MT5_LOGIN")),
            password=os.getenv("MT5_PASSWORD"),
            server=os.getenv("MT5_SERVER"),
            timeout=int(os.getenv("MT5_TIMEOUT")),
            portable=eval(os.getenv("MT5_PORTABLE"))):
            print("La plataforma MT5 se ha lanzado con exito!!!!")
        else:
            raise Exception(f"Ha ocurrido un error al inicializar la plataforma MT5: {mt5.last_error()}")

    def _live_account_warning(self) -> None:

        # Recuperamos el objeto de tipo accountinfo
        account_info = mt5.account_info()

        # Comprobar el tipo de cuenta que se ha lanzado
        if account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO:
            print("cuenta de tipo DEMO detectada")
        elif account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_REAL:
            if not input("ALERTA! Cuenta de tipo REAL detectada. Capital en riesgo. ¿Deseas continuar? (y/n): ").lower() == "y":
                mt5.shitdown()
                raise Exception("Usuario ha decidido DETENER el programa.")
        else:
            print("Cuenta de tipo CONCURSO detectada")
    
    def _check_algo_tradin_enable(self) -> None:

        # Vamos a comprobar que el trading algoritmico esta activado
        if not mt5.terminal_info().trade_allowed:
            raise Exception("El trading algoritmico está desactivado. Por favor, activalo MANUALMENTE!")
    
    def _add_symbols_to_maretwatch(self, symbols: list) -> None:

        # 1) Comprobar si el simbolo ya esta visible en el MW
        # 2) Si no lo esta, lo añadiremos
        for symbol in symbols:
            if mt5.symbol_info(symbol) is None:
                print(f"No se ha podido añadir el simbolo {symbol} al MarketWatch: {mt5.last_error()}")
                continue
            if not mt5.symbol_info(symbol).visible:
                if not mt5.symbol_select(symbol, True):
                    print(f"No se ha podido añadir el simbolo {symbol} al MarketWatch: {mt5.last_error()}")
                else:
                    print(f"Simbolo {symbol} se ha añadido con exito al MarketWatch")
            else:
                print(f"El simbolo {symbol} ya estaba en el Marketwatch.")
    
    def _print_account_info() -> None:

        # Recuperar un objeto de tipo AccountInfo
        account_info = mt5.account_info().asdict() 

        print(f"+------------ Informacion de la cuenta -------------")
        print(f"| - ID de cuenta: {account_info['login']}")
        print(f"| - Nombre trader: {account_info['name']}")
        print(f"| - Broker: {account_info['company']}")
        print(f"| - Servidor: {account_info['server']}")
        print(f"| - Apalancamiento: {account_info['currency']}")
        print(f"| - Balance de la cuenta: {account_info['balance']}")
        print(f"+---------------------------------------------------")