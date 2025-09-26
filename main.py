"""
main.py - Núcleo principal de ARGOTH-TRADER-BETA
-------------------------------------------------
Inicializa el entorno de trading, conecta con brokers
(simulación o real), carga la estrategia base (EMA50/EMA200 + RSI14)
y ejecuta un bucle que genera señales y registra datos.
"""

import os
import platform
import time
import pandas as pd
from config import SYMBOL, MT5_LOGIN, MT5_PASSWORD, MT5_SERVER
from strategy import generate_signals
from utils_sim import get_price_data  # simulador temporal
from utils_ibkr import connect_ibkr, get_accout_info


# ===============================
# CONFIGURACIÓN
# ===============================
DATA_FILE = "data/precios.csv"
OUTPUT_FILE = "data/signals_log.csv"

# Crear carpeta data si no existe
if not os.path.exists("data"):
    os.makedirs("data")

# ===============================
# IMPORTS DEPENDIENDO DEL SISTEMA
# ===============================
if platform.system() == "Windows":
    from utils_mt5 import connect, get_tick, shutdown
else:
    from utils_sim import get_tick  # Simulador para macOS/Linux

# ===============================
# FUNCIONES PRINCIPALES
# ===============================
def connect_brokers():
    """Conectar a brokers reales o simulados."""
    ok_mt5 = connect(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER)
    print(f"🔗 Conexión MT5 exitosa: {ok_mt5}")

    ok_ibkr = connect_ibkr()
    print(f"🔗 Conexión IBKR exitosa: {ok_ibkr}")

    return ok_mt5, ok_ibkr

def main_loop():
    """Loop principal que obtiene ticks y ejecuta estrategia, se detiene si hay problema."""
    try:
        while True:
            bid, ask = get_tick(SYMBOL)

            # Revisar si MT5 está desconectado o tick inválido
            if bid is None or ask is None:
                print("⚠️ Tick no recibido o desconexión detectada. Pausando ARGOTH...")
                break  # salir del loop, puedes usar 'return' o 'break'

            timestamp = pd.Timestamp.now()
            print(f"{timestamp} | Bid: {bid} | Ask: {ask}")

            # Generar señales a partir de un DataFrame simulado
            df = get_price_data(SYMBOL)       # 🔹 obtiene datos de precios
            signals = generate_signals(df)    # 🔹 genera señales

            # Si la señal es None (sin oportunidad de trading)
            if signals is None or len(signals) == 0:
                print("ℹ️ No hay señal válida, ARGOTH espera el siguiente tick...")
                time.sleep(1)
                continue  # esperar siguiente tick

            # Aquí ejecutas la lógica de trading según 'signals'
            print("📊 Señales generadas:", signals)
            # execute_trade(signals)

            time.sleep(1)

    except KeyboardInterrupt:
        print("🛑 ARGOTH detenido por usuario.")
        if platform.system() == "Windows":
            shutdown()

def main():
    """Función principal de ARGOTH."""
    print(f"🚀 ARGOTH iniciando con estrategia base para {SYMBOL}")

    # Conectar brokers
    connect_brokers()

    # Cargar datos históricos (simulación temporal)
    df = get_price_data(SYMBOL, DATA_FILE)
    if df is None or df.empty:
        print("⚠️ No se encontraron datos de precios. Verifica el archivo CSV.")
    else:
        # Generar señales con la estrategia
        df = generate_signals(df)

        # Mostrar últimas señales
        print("\n📊 Últimas 10 señales generadas:")
        print(df[["close", "EMA50", "EMA200", "RSI14", "Signal"]].tail(10))

        # Guardar log en CSV
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\n✅ Señales guardadas en {OUTPUT_FILE}")

    # Iniciar loop en tiempo real
    main_loop()

# ===============================
# EJECUCIÓN
# ===============================
if __name__ == "__main__":
    main()