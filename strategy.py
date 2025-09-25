"""
strategy.py - Estrategia base de ARGOTH
--------------------------------------
Implementa:
- EMA50 y EMA200
- RSI14
- Señales de compra/venta básicas

Flujo:
1. Calcular EMAs y RSI.
2. Generar señal:
   - BUY si EMA50 > EMA200 y RSI < 30 (sobreventa)
   - SELL si EMA50 < EMA200 y RSI > 70 (sobrecompra)
   - NONE en caso contrario
"""

import pandas as pd

def calculate_ema(df, period, column="close"):
    """
    Calcula el Exponential Moving Average (EMA) de un dataframe.
    
    df: DataFrame con columna 'close'
    period: número de periodos de la EMA
    column: columna sobre la cual calcular la EMA
    """
    ema = df[column].ewm(span=period, adjust=False).mean()
    return ema

def calculate_rsi(df, period=14, column="close"):
    """
    Calcula el Relative Strength Index (RSI) de un dataframe.
    
    df: DataFrame con columna 'close'
    period: número de periodos
    column: columna sobre la cual calcular RSI
    """
    delta = df[column].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signals(df):
    """
    Genera señales de trading usando EMA50/EMA200 y RSI14.
    
    df: DataFrame con columna 'close'
    
    Devuelve el mismo DataFrame con columnas agregadas:
    - EMA50
    - EMA200
    - RSI14
    - Signal: "BUY", "SELL", "NONE"
    """
    df["EMA50"] = calculate_ema(df, 50)
    df["EMA200"] = calculate_ema(df, 200)
    df["RSI14"] = calculate_rsi(df, 14)

    signals = []

    for i in range(len(df)):
        if df["EMA50"].iloc[i] > df["EMA200"].iloc[i] and df["RSI14"].iloc[i] < 30:
            signals.append("BUY")
        elif df["EMA50"].iloc[i] < df["EMA200"].iloc[i] and df["RSI14"].iloc[i] > 70:
            signals.append("SELL")
        else:
            signals.append("NONE")

    df["Signal"] = signals
    return df
