import config
import utils_sim
import utils_mt5
import utils

# utils_mt5.py (placeholder en CodeSpaces)
def get_tick(symbol):
    raise NotImplementedError("Solo funciona en Windows con MT5 Instalado")

SYMBOLS = "EURUSD"

def connect_mt5():
    print("🔌[SIMULACION ACTIVADA] Conexion MT5 establecida.")
    return True

def get_tick(symbol=SYMBOLS):
    #Devolver ticks fiticios para probar la logica 
    bid = 1.1000
    ask = 1.1002
    return bid, ask

def shutdown_mt5():
    print("🔌[SIMULACION ACTIVADA] MT5 desconectado.")

