try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None #MT5 no esta disponible, evita que truene en entornos sin MT5    
 
import config
import utils_sim
import utils_mt5
import utils

def get_tick(symbol):
    """Obtiene el ultimo precio Bid/Ask de un simbolo"""
    if not mt5.symbol_select(symbol, True): 
        return None
    tick = mt5.symbol_info_tick(symbol)
    return tick.bid, tick.ask