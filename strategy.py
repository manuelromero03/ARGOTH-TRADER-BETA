"""
strategy.py - Estrategia base de ARGOTH
--------------------------------------
Implementa:
- EMA50 y EMA200
- RSI14 (versión Wilder)
- Señales de compra/venta básicas
"""

import pandas as pd
import numpy as np


def calculate_ema(df, period, column="close"):
    """Calcula el Exponential Moving Average (EMA)."""
    return df[column].ewm(span=period, adjust=False).mean()


def calculate_rsi(df, period=14, column="close"):
    """Calcula el Relative Strength Index (RSI) con método de Wilder."""
    delta = df[column].diff()

    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    gain_ema = pd.Series(gain).ewm(alpha=1/period, adjust=False).mean()
    loss_ema = pd.Series(loss).ewm(alpha=1/period, adjust=False).mean()

    rs = gain_ema / (loss_ema.replace(0, 1e-10))  # evitar división por 0
    rsi = 100 - (100 / (1 + rs))

    return rsi


def generate_signals(df):
    """
    Genera señales de trading usando EMA50/EMA200 y RSI14.
    Retorna el DataFrame con nuevas columnas.
    """
    df["EMA50"] = calculate_ema(df, 50)
    df["EMA200"] = calculate_ema(df, 200)
    df["RSI14"] = calculate_rsi(df, 14)

    # Debug: ver último valor de EMAs y RSI
    print(f"EMA50: {df['EMA50'].iloc[-1]:.5f} | EMA200: {df['EMA200'].iloc[-1]:.5f} | RSI14: {df['RSI14'].iloc[-1]:.2f}")

    # Señales
    df["Signal"] = np.where(
        (df["EMA50"] > df["EMA200"]) & (df["RSI14"] < 30), "BUY",
        np.where((df["EMA50"] < df["EMA200"]) & (df["RSI14"] > 70), "SELL", "NONE")
    )

    return df