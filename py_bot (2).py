# -*- coding: utf-8 -*-
# https://github.com/ccxt/ccxt/blob/master/examples/bots/py/spot-arbitrage-bot.py
#---------------------------------------------------------------------------------------
# descripcion de como debe ser el bot
# se debe tener dinero en cada exchange y en cada cripto para
# hacer efectivo el bot
# mas explicacion en el siguente url
# https://steemit.com/spanish/@mondeja/curso-de-programacion-de-criptomonedas-con-python-13-como-crear-un-bot-de-arbitraje-parte-1
# https://steemit.com/spanish/@mondeja/curso-de-programacion-de-criptomonedas-con-python-14-como-crear-un-bot-de-arbitraje-parte-2
#---------------------------------------------------------------------------------------
import asyncio
import os
#from random import randint
import sys
from pprint import pprint
import time
from time import gmtime, strftime
import socket
import logging

# Configurar el registro
logging.basicConfig(filename='log.txt', level=logging.DEBUG)

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt  # noqa: E402

print('CCXT Version:', ccxt.__version__)

##############################################################################################
# Bot de arbitraje simple que buscará oportunidades de arbitraje en los mercados al contado ##
# y ejecutarlos usando órdenes de mercado.                                                  ##
##############################################################################################

# opciones de bot
wait_time = 5 # segundos de espera entre cada consulta
paper_trading = True # establecer en falso para ejecutar operaciones realmente
excepciones = {}  # diccionario de posibles excepciones


exchanges = [
    ccxt.ace(),
    ccxt.alpaca(),
    ccxt.ascendex(),
    ccxt.bequant(),
    ccxt.bigone(),
    ccxt.binance(),
    ccxt.binancecoinm(),
    ccxt.binanceus(),
    ccxt.binanceusdm(),
    ccxt.bit2c(),
    ccxt.bitbank(),
    ccxt.bitbay(),
    ccxt.bitbns(),
    ccxt.bitcoincom(),
    ccxt.bitfinex(),
    ccxt.bitfinex2(),
    ccxt.bitflyer(),
    ccxt.bitforex(),
    ccxt.bitget(),
    ccxt.bithumb(),
    ccxt.bitmart(),
    ccxt.bitmex(),
    ccxt.bitopro(),
    ccxt.bitpanda(),
    ccxt.bitrue(),
    ccxt.bitso(),
    ccxt.bitstamp(),
    ccxt.bitstamp1(),
    ccxt.bittrex(),
    ccxt.bitvavo(),
    ccxt.bkex(),
    ccxt.bl3p(),
    ccxt.blockchaincom(),
    ccxt.btcalpha(),
    ccxt.btcbox(),
    ccxt.btcex(),
    ccxt.btcmarkets(),
    ccxt.btctradeua(),
    ccxt.btcturk(),
    ccxt.buda(),
    ccxt.bybit(),
    ccxt.cex(),
    ccxt.coinbase(),
    ccxt.coinbaseprime(),
    ccxt.coinbasepro(),
    ccxt.coincheck(),
    ccxt.coinex(),
    ccxt.coinfalcon(),
    ccxt.coinmate(),
    ccxt.coinone(),
    ccxt.coinsph(),
    ccxt.coinspot(),
    ccxt.cryptocom(),
    ccxt.currencycom(),
    ccxt.delta(),
    ccxt.deribit(),
    ccxt.digifinex(),
    ccxt.exmo(),
    ccxt.flowbtc(),
    ccxt.fmfwio(),
    ccxt.gate(),
    ccxt.gateio(),
    ccxt.gemini(),
    ccxt.hitbtc(),
    ccxt.hitbtc3(),
    ccxt.hollaex(),
    ccxt.huobi(),
    ccxt.huobijp(),
    ccxt.huobipro(),
    ccxt.idex(),
    ccxt.independentreserve(),
    ccxt.indodax(),
    ccxt.itbit(),
    ccxt.kraken(),
    ccxt.krakenfutures(),
    ccxt.kucoin(),
    ccxt.kucoinfutures(),
    ccxt.kuna(),
    ccxt.latoken(),
    ccxt.lbank(),
    ccxt.lbank2(),
    ccxt.luno(),
    ccxt.lykke(),
    ccxt.mercado(),
    ccxt.mexc(),
    ccxt.mexc3(),
    ccxt.ndax(),
    ccxt.novadax(),
    ccxt.oceanex(),
    ccxt.okcoin(),
    ccxt.okex(),
    ccxt.okex5(),
    ccxt.okx(),
    ccxt.paymium(),
    ccxt.phemex(),
    ccxt.poloniex(),
    ccxt.poloniexfutures(),
    ccxt.probit(),
    ccxt.ripio(),
    ccxt.stex(),
    ccxt.tidex(),
    ccxt.timex(),
    ccxt.tokocrypto(),
    ccxt.upbit(),
    ccxt.wavesexchange(),
    ccxt.wazirx(),
    ccxt.whitebit(),
    ccxt.woo(),
    ccxt.xt(),
    ccxt.yobit(),
    ccxt.zaif(),
    ccxt.zonda(),
    ] # lista de exchanges a consultar

symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'DOGE/USDT', 'ADA/USDT', 'XRP/USDT', 'SOL/USDT', 'DOT/USDT', 'LTC/USDT', 'UNI/USDT', 'MATIC/USDT', 'THETA/USDT', 'BCH/USDT', 'LINK/USDT', 'VET/USDT', 'FIL/USDT', 'ETC/USDT', 'TRX/USDT', 'EOS/USDT', 'XLM/USDT', 'AAVE/USDT', 'COMP/USDT', 'MKR/USDT', 'SNX/USDT', 'YFI/USDT', 'ZEC/USDT', 'ZRX/USDT', '1INCH/USDT', 'SUSHI/USDT', 'CAKE/USDT'] # lista de pares de criptomonedas a consultar

# intercambios que desea utilizar para buscar oportunidades de arbitraje

"""exchanges = [
    ccxt.okx(),
    ccxt.bybit({"options":{"defaultType":"spot"}}),
    ccxt.binance(),
    ccxt.kucoin(),
    ccxt.bitmart(),
    ccxt.kraken(),
    ccxt.gate()
]
"""

# símbolos que desea intercambiar
"""symbols = [
    "BTC/USDT",
    "LTC/USDT",
    "DOGE/USDT",
    "SHIB/USDT",
    "SOL/USDT",
    "ETH/USDT",
    "ADA/USDT",
    "DOT/USDT",
    "UNI/USDT",
    "LINK/USDT",
]
""" 

# Pide tamaños para cada símbolo, ajustar a conveniencia
order_sizes = {
    "BTC/USDT": 0.001,
    "LTC/USDT": 0.01,
    "DOGE/USDT": 100,
    "SHIB/USDT": 1000000,
    "SOL/USDT": 0.1,
    "ETH/USDT": 0.01,
    "ADA/USDT": 1,
    "DOT/USDT": 0.1,
    "UNI/USDT": 0.1,
    "LINK/USDT": 0.1,
}

async def get_last_prices():
    
    #tasks = [ 
    #    exchange.fetch_tickers(symbols) for exchange in exchanges 
    #    ]
    
    temp_symbols = symbols.copy()    
    tasks = []

    for exchange in exchanges:
        for consultar in excepciones:
            #print (exchange.id,":", consultar, excepciones[consultar])
            if exchange.id == consultar:
                #print( exchange.id, temp_symbols)
                temp_symbols.remove(excepciones[consultar]) 
                

        tasks.append(exchange.fetch_tickers(temp_symbols))

    #print (type (tasks))
    results = await asyncio.gather(*tasks)
    return results
    
async def bot():
    try:

        prices = await get_last_prices()
        for symbol in symbols:
            #ms = int(time.time() * 1000)
            #if symbol == "UNI/USDT":
            #    print ("kentoki")

            symbol_prices =[]
            mss = strftime("%d %b %Y %H:%M:%S ", gmtime())

            #symbol_prices = [ exchange_prices[symbol]['last'] for exchange_prices in prices ]
            
            for exchange_prices in prices:

                #print ("exchange_prices:",exchange_prices, " symbol:", symbol)
                #pprint(exchange_prices)

                if (symbol in exchange_prices):
                    #print ("encontrado")
                    symbol_prices.append(exchange_prices[symbol]['last'])
                else:
                    symbol_prices.append(0)
                    #print ("no encontrado")

                

            min_price = min(symbol_prices)
            max_price = max(symbol_prices)

            order_size = order_sizes[symbol]

            min_exchange = exchanges[symbol_prices.index(min_price)]
            max_exchange = exchanges[symbol_prices.index(max_price)]

            # calcular la tarifa mínima del tomador de cambio
            # advertencia: se debe verificar manualmente si hay tarifas de campaña especiales
            min_exchange_fee = min_exchange.fees['trading']['taker']
            min_fee = order_size * min_price * min_exchange_fee

            # calcular la tarifa máxima del tomador de intercambio
            # advertencia: se debe verificar manualmente si hay tarifas de campaña especiales
            max_exchange_fee = max_exchange.fees['trading']['taker']
            max_fee = order_size * max_price * max_exchange_fee

            price_profit = max_price - min_price
            profit = (price_profit * order_size) - (min_fee) - (max_fee)

            if (profit > 0): # sin tener en cuenta el deslizamiento o la profundidad de la cartera de pedidos
                print("#----------------------------------------------------------------------#")
                print(str(mss), symbol, "ganancia:", profit, "Comprar", min_exchange.id, min_price, "Vender", max_exchange.id, max_price)
               
                print(" ------ symbol prices:",symbol_prices,"precio minimo:",min_price, "precio maximo:",max_price)
                print(" ------ min_exchange:",min_exchange,"max_exchange:",max_exchange)
                print(" ------ min_exchange_fee:",min_exchange_fee,"min_fee:",min_fee)
                print(" ------ max_exchange_fee:",max_exchange_fee,"min_fee:",max_fee)
                print(" ------ price_profit:",price_profit)
                print("#----------------------------------------------------------------------#")

                if not paper_trading:
                    buy_min = min_exchange.create_market_buy_order(symbol, order_size)
                    sell_max = max_exchange.create_market_sell_order(symbol, order_size)
                    orders = await asyncio.gather(buy_min, sell_max) # se ejecutan simultáneamente
                    print("Órdenes ejecutadas con éxito")
            else:
                print(str(mss), symbol, "sin oportunidad de arbitraje")

    except Exception as e:
        print(f'Fallado con: {e}')

async def check_requirements():
    try:
        print("Comprobando si los intercambios admiten fetchTickers y los símbolos que queremos intercambiar")
        logging.debug("Comprobando si los intercambios admiten fetchTickers y los símbolos que queremos intercambiar")
        for exchange in exchanges:
            pprint (exchange)
            logging.debug(exchange)
            if not exchange.has['fetchTickers']:
                print(exchange.id, "no es compatible con fetchTickers")
                logging.debug("no es compatible con fetchTickers")
                #sys.exit()

            await exchange.load_markets()
            
            for symbol in symbols:
                if symbol not in exchange.markets:
                    excepciones[exchange.id] = symbol
                    print (symbol,"..........[Error!]")        
                    logging.debug("..........[Error!]")
                    #sys.exit()
                else:
                    print (symbol,"..............[ok]")
                    logging.debug("..............[ok]")

    except Exception as e:
        print(f'Fallado con: {e}')
                            

def chequear_Internet():
    status= False
    print ("chequeando Internet")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        # comprobamos si tiene conexión a internet por medio de socket
        s.connect(("www.google.com", 80))    
    except (socket.gaierror, socket.timeout):
        print("Sin conexión a internet")
        status = True
    else:
        print("Con conexión a internet")
        s.close()
                
    return status

async def main():
    await check_requirements()
    print("Despertando el Bot")
    
    while True:
        
        try:
            print ("*******************")
            await bot()
        
        except Exception as e:
            print(f'Fallado con: {e}')
        
        await asyncio.sleep(wait_time)


asyncio.run(main())


mi_lista=[]

for i in range(5):
    if i!=2:
        text = "%i- hola mundo" % i
        mi_lista.append(text)