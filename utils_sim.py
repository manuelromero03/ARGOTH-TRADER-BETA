"""
utils_sim.py - Simulador de mercado para ARGOTH
------------------------------------------------
Este módulo permite probar ARGOTH sin conexión real a brokers.
Incluye funciones para obtener ticks y datos históricos simulados.
"""

import random
import pandas as pd

# Símbolo por defecto
SYMBOLS = ["EURUSD", "BTCUSD", "XAUUSD"]

def get_tick(symbol="EURUSD"):
    """
    Devuelve un tick simulado: bid y ask.
    """
    bid = round(random.uniform(1.08, 1.12), 5)
    ask = round(bid + 0.0002, 5)
    return bid, ask

def get_price_data(symbol="EURUSD", file_path=None, n=50):
    """
    Genera un DataFrame simulado de precios históricos.
    - symbol: nombre del símbolo
    - file_path: si se pasa, guarda CSV
    - n: cantidad de ticks a generar
    """
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="1min")
    data = {
        "timestamp": timestamps,
        "open": [round(random.uniform(1.08, 1.12), 5) for _ in range(n)],
        "high": [round(random.uniform(1.08, 1.12), 5) for _ in range(n)],
        "low": [round(random.uniform(1.08, 1.12), 5) for _ in range(n)],
        "close": [round(random.uniform(1.08, 1.12), 5) for _ in range(n)],
        "volume": [random.randint(100, 1000) for _ in range(n)]
    }
    df = pd.DataFrame(data)

    if file_path:
        df.to_csv(file_path, index=False)
    
    return df

if __name__ == "__main__":
    # Test rápido
    print("Tick de prueba:", get_tick())
    df = get_price_data()
    print("\nDatos históricos simulados:\n", df.head())