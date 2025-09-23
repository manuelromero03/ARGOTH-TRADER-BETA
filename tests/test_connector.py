"""
test_connector.py - Pruebas rápidas para utils_mt5 y utils_ibkr
---------------------------------------------------------------
Este script permite validar la conexión (real o simulada) de ARGOTH
con MetaTrader5 y Interactive Brokers. 
"""

from utils_mt5 import connect, get_tick, shutdown
from utils_ibkr import connect_ibkr, get_accout_info  # coincide con tu archivo actual

def test_mt5():
    """Prueba de conexión a MT5 y obtiene un tick de ejemplo."""
    print("\n=== TEST MT5 ===")
    ok = connect()
    print(f"¿Conectado a MT5? {ok}")
    bid, ask = get_tick("EURUSD")
    print(f"EURUSD -> Bid: {bid}, Ask: {ask}")
    shutdown()

def test_ibkr():
    """Prueba de conexión a IBKR y obtiene información de cuenta."""
    print("\n=== TEST IBKR ===")
    ok = connect_ibkr()
    print(f"¿Conectado a IBKR? {ok}")
    print("Cuenta:", get_accout_info())

if __name__ == "__main__":
    test_mt5()
    test_ibkr()