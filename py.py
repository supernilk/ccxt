import ccxt

def obtener_precio(exchange):
    #binance = ccxt.binance()
    #exchange = binance
    precio = exchange.fetch_ticker('DOGE/USDT')['last']
    print (exchange.name , ":" , precio)


binance = ccxt.binance()
kraken = ccxt.kraken()
bitget = ccxt.bitget()


obtener_precio(binance)
obtener_precio(kraken)
obtener_precio(bitget)