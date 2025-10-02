"""
main.py - Núcleo principal de ARGOTH-TRADER-BETA
-------------------------------------------------
Inicializa el entorno de trading, conecta con brokers
(simulación o real), carga la estrategia base (EMA50/EMA200 + RSI14)
y ejecuta un bucle que genera señales y registra datos.
"""

import csv
import sqlite3
import os
import platform
import time
import pandas as pd
from datetime import datetime
from tabulate import tabulate
from colorama import Fore, Style, init

import MetaTrader5 as mt5

# Configuración interna
from config import SYMBOL, MT5_LOGIN, MT5_PASSWORD, MT5_SERVER
from strategy import generate_signals
from utils_sim import get_price_data  # simulador temporal
from utils_ibkr import connect_ibkr, get_accout_info

# Inicializar colorama
init(autoreset=True)

# ===============================
# BASE DE DATOS
# ===============================
conn = sqlite3.connect("argoth_trading.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    timestamp TEXT,
    symbol TEXT,
    bid REAL,
    ask REAL,
    signal TEXT,
    lot_size REAL,
    sl REAL,
    tp REAL,
    close REAL,
    ema50 REAL,
    ema200 REAL,
    rsi14 REAL
)
""")
conn.commit()

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
# PARAMETROS DE RIESGO
# ===============================
RISK_PERCENT = 1        # 1% de capital a arriesgar por operación
STOP_LOSS_PIPS = 20     # Stop Loss en pips
TAKE_PROFIT_PIPS = 40   # Take Profit en pips


def calculate_lot_size(balance, risk_percent, stop_loss_pips, pip_value=0.0001):
    """Calcula el tamaño de lote basado en capital y riesgo."""
    risk_amount = balance * (risk_percent / 100)
    lot_size = risk_amount / (stop_loss_pips * pip_value * 100000)  # 1 lote estándar = 100k
    return round(lot_size, 2)


def color_signal(signal: str) -> str:
    """Devuelve la señal con color según BUY/SELL/None."""
    if signal == "BUY":
        return Fore.GREEN + signal + Style.RESET_ALL
    elif signal == "SELL":
        return Fore.RED + signal + Style.RESET_ALL
    else:
        return Fore.YELLOW + (signal if signal else "NONE") + Style.RESET_ALL


# ===============================
# FUNCIONES AUXILIARES
# ===============================
def save_to_csv_and_sql(timestamp, symbol, bid, ask, signal, lot_size, sl, tp, close, ema50, ema200, rsi14):
    """Guardar operación en CSV + SQLite."""
    # CSV
    with open("signal_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, symbol, bid, ask, signal, lot_size, sl, tp, close, ema50, ema200, rsi14])

    # SQL
    cursor.execute("""
    INSERT INTO trades (timestamp, symbol, bid, ask, signal, lot_size, sl, tp, close, ema50, ema200, rsi14)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, symbol, bid, ask, signal, lot_size, sl, tp, close, ema50, ema200, rsi14))
    conn.commit()


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


def save_trade_to_db(timestamp, symbol, bid, ask, signal, lot_size, sl, tp, close, ema50, ema200, rsi14):
    """
    Inserta un registro de trade en la tabla `trades`. Usa las variables globales
    `conn` y `cursor` que ya definiste al inicio del archivo.
    """
    # normalizar timestamp a string
    if hasattr(timestamp, "isoformat"):
        ts = timestamp.isoformat()
    else:
        ts = str(timestamp)

    # asegurar tipos float (evita errores si vienen como numpy types)
    try:
        bid_v = float(bid) if bid is not None else None
        ask_v = float(ask) if ask is not None else None
        close_v = float(close) if close is not None else None
        ema50_v = float(ema50) if ema50 is not None else None
        ema200_v = float(ema200) if ema200 is not None else None
        rsi_v = float(rsi14) if rsi14 is not None else None
    except Exception:
        bid_v = ask_v = close_v = ema50_v = ema200_v = rsi_v = None

    cursor.execute("""
        INSERT INTO trades
        (timestamp, symbol, bid, ask, signal, lot_size, sl, tp, close, ema50, ema200, rsi14)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ts, symbol, bid_v, ask_v, signal, lot_size, sl, tp, close_v, ema50_v, ema200_v, rsi_v))
    conn.commit()

# ===============================
# LOOP PRINCIPAL
# ===============================
def main_loop():
    """Loop principal que obtiene ticks y ejecuta estrategia."""
    try:
        account_balance = 10000  # demo inicial (TODO: reemplazar con get_account_info())

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

            # Calcular SL, TP y lotes SOLO si hay señal
            if last_signal in ["BUY","SELL"]:
                lot_size = calculate_lot_size(account_balance, RISK_PERCENT, STOP_LOSS_PIPS)
                if last_signal == "BUY":
                    sl_price = bid - STOP_LOSS_PIPS * 0.0001
                    tp_price = bid + TAKE_PROFIT_PIPS * 0.0001
                else:
                    sl_price = bid + STOP_LOSS_PIPS * 0.0001
                    tp_price = bid - TAKE_PROFIT_PIPS * 0.0001

                # Debug en consola
                print(f"📊 Señal actual: {color_signal(last_signal)} | Lote:{lot_size} | SL:{sl_price:.5f} | TP:{tp_price:.5f}")
                print(f"   ➡️ Close: {last_close:.5f} | EMA50: {last_ema50:.5f} | EMA200: {last_ema200:.5f} | RSI14: {last_rsi:.2f}")

                try:
                    save_to_csv_and_sql(timestamp, SYMBOL, bid, ask, last_signal,
                            lot_size, sl_price, tp_price,
                            last_close, last_ema50, last_ema200, last_rsi)
                except NameError:
                    pass

                save_trade_to_db(timestamp, SYMBOL, bid, ask, last_signal,
                                 lot_size, sl_price, tp_price,
                                 last_close, last_ema50, last_ema200, last_rsi)

                # Guardar registro
                # Guardar en la base de datos
                save_trade_to_db(
                                last_signal, 
                                bid if last_signal == "BUY" else ask, 
                                lot_size, 
                                sl_price, 
                                tp_price, 
                                "OPEN"
                                )

                # Aquí va la ejecución de órdenes reales
                # execute_trade(last_signal)

            else:
                print("ℹ️ No hay señal válida, esperando siguiente tick...")

            time.sleep(1)

    except KeyboardInterrupt:
        print("🛑 ARGOTH detenido por usuario.")
        if platform.system() == "Windows":
            shutdown()


# ===============================
# MAIN
# ===============================
def main():
    print(f"🚀 ARGOTH iniciando con estrategia base para {SYMBOL}")

    # Conectar brokers
    connect_brokers()

    # Cargar datos históricos (simulación temporal)
    df = get_price_data(SYMBOL, DATA_FILE)
    if df is None or df.empty:
        print("⚠️ No se encontraron datos de precios. Verifica el archivo CSV.")
    else:
        df = generate_signals(df)

        # Reordenamos columnas
        columns_order = ["time","close","EMA50","EMA200","RSI14","Signal"]
        df = df[[c for c in columns_order if c in df.columns]]

        # Colorear columna Signal
        df_color = df.copy()
        df_color["Signal"] = df_color["Signal"].apply(color_signal)

        print("\n📊 Últimas 10 señales generadas:")
        print(tabulate(df_color.tail(10),
                      headers="keys",
                      tablefmt="psql",
                      floatfmt=".5f"))

        df.to_csv(OUTPUT_FILE, index=False, float_format="%.5f")
        print(f"\n✅ Señales guardadas en {OUTPUT_FILE}")

    # Loop en tiempo real
    main_loop()


if __name__ == "__main__":
    main()