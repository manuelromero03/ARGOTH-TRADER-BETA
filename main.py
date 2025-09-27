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
from utils_ibkr import connect_ibkr, get_accout_info  # ✅ corregido
import MetaTrader5 as mt5

# ===============================
# CONFIGURACIÓN
# ===============================
DATA_FILE = "data/precios.csv"
OUTPUT_FILE = "data/signals_log.csv"
SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_M1
N_CANDLES = 250

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
    if platform.system() == "Windows":
        ok_mt5 = connect(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER)
        print(f"🔗 Conexión MT5 exitosa: {ok_mt5}")
    else:
        ok_mt5 = False
        print("⚠️ MT5 no disponible en este sistema (usando simulador).")

    ok_ibkr = connect_ibkr()
    print(f"🔗 Conexión IBKR exitosa: {ok_ibkr}")

    return ok_mt5, ok_ibkr


def get_candles(symbol, n=250, timeframe=TIMEFRAME):
    """Descargar velas del activo desde MT5."""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)
    if rates is None or len(rates) == 0:
        return None
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df


def main_loop():
    """Loop principal que obtiene ticks y ejecuta estrategia, se detiene si hay problema."""
    try:
        while True:
            bid, ask = get_tick(SYMBOL)

            if bid is None or ask is None:
                print("⚠️ Tick no recibido o desconexión detectada. Pausando ARGOTH...")
                break

            timestamp = pd.Timestamp.now()
            print(f"\n{timestamp} | Bid: {bid} | Ask: {ask}")

            # Generar señales
            df = get_price_data(SYMBOL)
            df_signals = generate_signals(df)

            # Últimos valores
            last_close = df_signals["close"].iloc[-1]
            last_ema50 = df_signals["EMA50"].iloc[-1]
            last_ema200 = df_signals["EMA200"].iloc[-1]
            last_rsi = df_signals["RSI14"].iloc[-1]
            last_signal = df_signals["Signal"].iloc[-1]

            # Debug en consola
            print(f"📊 Señal actual: {last_signal}")
            print(f"   ➡️ Close: {last_close:.5f} | EMA50: {last_ema50:.5f} | EMA200: {last_ema200:.5f} | RSI14: {last_rsi:.2f}")

            # Aquí ejecutas la lógica de trading según 'last_signal'
            # execute_trade(last_signal)

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