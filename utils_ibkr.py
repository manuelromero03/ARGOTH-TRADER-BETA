"""
utils_ibkr.py
--------------------------------------
conector placeholder para Interactive Brokers (IBKR).
Este archivo servira como base para integrar la API de IBKR en el futuro.

Pon ahora solo expone funciones simuladas para que los test pasen 
"""

import sys 
import os 
# Asegura que Python vea la carpeta raiz del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def connect_ibkr():
    """
    Simulacion de conexion a Interative Brokers.
    En la version real, usaremos la API oficial de IBKR/TWS o IB Gateway.
    """
    print("🔌[SIMULACION ACTIVADA] Conexion a IBKR establecidad.")
    return True

def get_accout_info(): 
    """
    Devuelve informacion ficticia de la cuenta IBKR.
    """
    return {"account_id": "SIM12345", "balance": 100000}