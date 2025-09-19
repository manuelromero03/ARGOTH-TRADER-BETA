"""
Test basico de conectores para ARGOTH
-------------------------------------
Verifica que los modulos de conexion (MT5 e IBKR) esten disponibleS.
Este test no abre conexion real en Codespaces solo asegura la estructura.
"""

import sys
import os

# Añade la carpeta raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import importlib

def test_module(name):
    try:
        importlib.import_module(name)
        print(f"[OK] {name} importado correctamente ✅")
    except ModuleNotFoundError:
        print(f"[FAIL] {name} no encontrado ❌")
    except Exception as e: 
        print(f"[ERROR] Error al importar {name}: {e} ❌")
        
if __name__== "__main__":
     print("🔍 Verificando de conectores ARGOTH.../n")
     test_module("utils_mt5")
     test_module("utils_ibkr") #no creado aun sera un placeholder
     test_module("utils_sim") #simulador interno
     print("/n✅ Test de conectores finalizado.")
     
    
     