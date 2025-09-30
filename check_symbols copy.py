import MetaTrader5 as mt5

#Inicializar MT5
if not mt5.initialize():
    print("❌ No se pudo inicializar MT5")
    quit()

#Obtener todos los symbols visibles en MT5
symbols = mt5.symbols_get()

print(f"Se encontraron {len(symbols)} simbolos\n")

#Mostrar solo los primeros 50 para no saturar 
for s in symbols[:50]:
    print(s.name)


#Cerrar Conexion 
mt5.shutdown()
