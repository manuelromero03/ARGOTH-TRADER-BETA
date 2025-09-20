"""
utils_mt5.py - Conector MetaTrader 5 para ARGTOTH
--------------------------------------------------
Modulo encargado de la conexion con MetaTrader 5.
En Codespaces funciona como placeHolder(sin Conexion real).
En windows con MT5 instalado, permitira: 
 -Login
 -Obtener datos de mercado 
 -Enviar ordenes 
"""

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    print("⚠️ MetaTrader5 no esta instalado en este entorno (placeholder activo).")
    MT5_AVAILABLE = False 

def connect(login: int = None, password: str = None, server: str = None) -> bool:
    """
    Intenta conector a MetaTrader 5.
    En Codespaces siempre devolvera False.
    """
    if not MT5_AVAILABLE:
        return False
    
    if not mt5.initialize(login=login, password=password, server=server):
        print(f"❌ Error al conector MT5: {mt5.last_error()}")
        return False 
    print("✅ Conexion establecida con MetaTrader 5.")
    return True 

def get_symbols():
    """
    Devuelve la lista de simbolos disponibles en MT5.
    En  codespaces devuelve lista simulada.
    """
    if not MT5_AVAILABLE: 
        return ["EURUSD", "BTCUSD", "XAUUSD (oro)"]

    Symbols = mt5.symbols_get()
    return [s.name for s in Symbols]

def shutrdown():
    """
    Cierra la conexion con MT5 si esta disponible.
    """
    if MT5_AVAILABLE:
        mt5.shutdown()
        print("🔌 Conexion con MT5 cerrada.")
    else: 
        print("⚠️ No hay conexion activa (placeholder).")
        