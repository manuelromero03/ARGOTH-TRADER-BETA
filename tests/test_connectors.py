"""
test_connectors.py - Pruebas rápidas de conectores ARGOTH
---------------------------------------------------------
Verifica que los módulos de conexión (MT5 e IBKR) estén disponibles
y realiza tests básicos de conexión y obtención de datos.
"""

import sys
import os
import importlib

# Añade la carpeta raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ===============================
# TEST DE IMPORTACIÓN
# ===============================
def test_module(name):
    try:
        importlib.import_module(name)
        print(f"[OK] {name} importado correctamente ✅")
    except ModuleNotFoundError:
        print(f"[FAIL] {name} no encontrado ❌")
    except Exception as e:
        print(f"[ERROR] Error al importar {name}: {e} ❌")

def test_imports():
    print("🔍 Verificando módulos de conectores ARGOTH...\n")
    test_module("utils_mt5")
    test_module("utils_ibkr")  # placeholder si no creado aún
    test_module("utils_sim")   # simulador interno
    print("\n✅ Test de conectores finalizado.\n")

# ===============================
# TEST DE CONEXIÓN
# ===============================
from utils_mt5 import connect, get_tick, shutdown
from utils_ibkr import connect_ibkr, get_accout_info

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

# ===============================
# EJECUCIÓN
# ===============================
if __name__ == "__main__":
    test_imports()
    test_mt5()
    test_ibkr()