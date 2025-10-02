"""
general_test.py Test rapido de estrategia ARGOTH 
------------------------------------------------
Carga datos historicos y muestra señales, EMA y RSI 
para las ultimas velas. Ideal para debug rapido.
"""

import pandas as pd 
import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from strategy import generate_signals

#Archivo CSV de precios
DATA_FILE = "data/precios.csv"

#Cargar Datos 
df = pd.read_csv(DATA_FILE)
if df.empty: 
    print("⚠ No se encontraron datos en", DATA_FILE)
    exit()

#Generar Señales
df_signals = generate_signals(df)

#Mostrar ultimas 10 señales con sus indicadores
print("\n📊 Ultimo 10 señales generadas:")
print(df_signals[["close", "EMA50", "EMA200", "RSI14", "Signal"]].tail(10))

#Ultima señal 
last_signal = df_signals["Signal"].iloc[-1]
print(f"\n 🚦 Señal actual: {last_signal}")

 