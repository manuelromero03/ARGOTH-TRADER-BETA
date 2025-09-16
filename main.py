import os 
if not os.path.exists("data"):
    os.makedirs("data")

import platform
from config import SYMBOL

if platform.system() == "Windows":
    from utils_mt5 import get_tick  # aquí sí MT5
else:
    from utils_sim import get_tick  # aquí simulador

# Ejemplo de loop
import pandas as pd
import time

columns = ["timestamp", "bid", "ask"]
df = pd.DataFrame(columns=columns)

for _ in range(5):
    bid, ask = get_tick(SYMBOL)
    timestamp = pd.Timestamp.now()
    df = pd.concat([df, pd.DataFrame([[timestamp, bid, ask]], columns=columns)], ignore_index=True)
    print(f"{timestamp} | Bid: {bid} | Ask: {ask}")
    time.sleep(1)

df.to_csv("data/precios.csv", index=False)
