"""
utils_mt5.py - Conector MetaTrader 5 para ARGOTH
--------------------------------------------------
Módulo encargado de la conexión con MetaTrader 5.
En Codespaces funciona como placeholder (sin conexión real).
En Windows con MT5 instalado, permitirá:
 - Login
 - Obtener datos de mercado
 - Enviar órdenes
"""

import random

# Intento importar MT5
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    print("⚠️ MetaTrader5 no está instalado en este entorno (placeholder activo).")
    MT5_AVAILABLE = False

def connect(login: int = None, password: str = None, server: str = None) -> bool:
    """
    Conecta a MT5. Si MT5 no está disponible, usa placeholder.
    """
    if not MT5_AVAILABLE:
        print("🔌 Placeholder activo, no se conecta a MT5 real.")
        return False

    if not mt5.initialize(login=login, password=password, server=server):
        print(f"❌ Error al conectar MT5: {mt5.last_error()}")
        return False

    print("✅ Conexión establecida con MT5.")
    return True

def get_symbols():
    """
    Devuelve la lista de símbolos disponibles en MT5.
    Si MT5 no está disponible, devuelve lista simulada.
    """
    if not MT5_AVAILABLE:
        return ["EURUSD", "BTCUSD", "XAUUSD (oro)"]

    symbols = mt5.symbols_get()
    return [s.name for s in symbols]

def get_tick(symbol):
    """
    Devuelve el último tick de mercado.
    Si MT5 no está disponible, devuelve valores simulados.
    """
    if MT5_AVAILABLE:
        tick = mt5.symbol_info_tick(symbol)
        if tick:
            return tick.bid, tick.ask
        else:
            return None, None
    else:
        # Simulación
        bid = round(random.uniform(1.08, 1.12), 5)
        ask = bid + 0.0002
        return bid, ask

def shutdown():
    """
    Cierra la conexión con MT5 si está disponible.
    """
    if MT5_AVAILABLE:
        mt5.shutdown()
        print("🔌 Conexión MT5 cerrada.")
    else:
        print("⚠️ Placeholder, no hay conexión real que cerrar.")