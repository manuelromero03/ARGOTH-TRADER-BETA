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

def get_tick(symbol: str = None):
    """
    Devolver ticks fiticios (simulacion) para probar la logica 
    Si se enjecuta en un entorno real con MT5 instalado
    Deberia llamar a mt5.symbol_info_tick.
    """
    bid = 1.1000
    ask = 1.1002
    return bid, ask

def shutdown_mt5():
    """
    Cierra la conexion con MT5 si esta activa. 
    """
    if MT5_AVAILABLE:
        mt5.shutdown()
        print("🔌 MT5 desconectado.")
    else: 
        print("🔌[SIMULACION ACTIVADA] MT5 desconectado.")

