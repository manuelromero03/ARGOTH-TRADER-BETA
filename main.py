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
    """Loop principal que obtiene ticks y ejecuta estrategia."""
    columns = ["timestamp", "bid", "ask"]
    df = pd.DataFrame(columns=columns)

    try:
        while True:
            bid, ask = get_tick(SYMBOL)
            timestamp = pd.Timestamp.now()
            df = pd.concat([df, pd.DataFrame([[timestamp, bid, ask]], columns=columns)], ignore_index=True)
            print(f"{timestamp} | Bid: {bid} | Ask: {ask}")

            # TODO: aquí luego puedes llamar a la estrategia
            # signals = generate_signals(...)

            # Guardar tick en CSV
            df.to_csv(DATA_FILE, index=False)

            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Parando ARGOTH...")
        if platform.system() == "Windows":
            shutdown()  # solo si usamos MT5 real

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