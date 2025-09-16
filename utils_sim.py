import random 

def get_tick(symbol):
    """Simula un tick de MT5"""
    bid = round(random.uniform(1.08,1.12), 5)
    ask = bid + 0.0002
    return bid, ask 

