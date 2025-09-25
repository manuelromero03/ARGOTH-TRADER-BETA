"""
utils_mt5.py - Conector MetaTrader 5 para ARGOTH
--------------------------------------------------
Módulo encargado de la conexión con MetaTrader 5.
- En Windows con MT5 instalado → conexión real.
- En otros entornos (ej. Codespaces) → modo simulación.
"""

import random

# Intento importar MetaTrader5
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    print("⚠️ MetaTrader5 no está instalado en este entorno (modo simulación activo).")
    MT5_AVAILABLE = False

# =========================
# Conexión
# =========================
def connect(login: int = None, password: str = None, server: str = None) -> bool:
    """
    Conecta a MT5. Si no está disponible, usa simulación.
    """
    if not MT5_AVAILABLE:
        print("🔌 [SIMULACIÓN] Conexión MT5 establecida.")
        return True

    if not mt5.initialize(login=login, password=password, server=server):
        print(f"❌ Error al conectar MT5: {mt5.last_error()}")
        return False

    print("✅ Conexión establecida con MT5 real.")
    return True

# =========================
# Obtener símbolos
# =========================
def get_symbols():
    """
    Devuelve lista de símbolos disponibles.
    """
    if not MT5_AVAILABLE:
        return ["EURUSD", "BTCUSD", "XAUUSD (oro)"]

    symbols = mt5.symbols_get()
    return [s.name for s in symbols]

# =========================
# Obtener ticks
# =========================
def get_tick(symbol="EURUSD"):
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
        # Simulación: precios ficticios
        bid = round(random.uniform(1.08, 1.12), 5)
        ask = bid + 0.0002
        return bid, ask

# =========================
# Cerrar conexión
# =========================
def shutdown():
    """
    Cierra la conexión con MT5.
    """
    if MT5_AVAILABLE:
        mt5.shutdown()
        print("🔌 Conexión MT5 cerrada.")
    else:
        print("⚠️ [SIMULACIÓN] No hay conexión real que cerrar.")
