import ccxt
import logging
import asyncio

# Configurar el registro
logging.basicConfig(filename='log.txt', level=logging.DEBUG)

def obtener_precio(exchange):
    #binance = ccxt.binance()
    #exchange = binance
    precio = exchange.fetch_ticker('DOGE/USDT')['last']
    print (exchange.name , ":" , precio)


binance = ccxt.binance()
kraken = ccxt.kraken()
bitget = ccxt.bitget()


#obtener_precio(binance)
#obtener_precio(kraken)
#obtener_precio(bitget)

"""
from colorama import init, Fore, Back, Style

# Para restablecer colores después de cada impresión inicializar 
# el módulo con init(autoreset=True) en lugar de init().

init()
print(Fore.RED+"Texto color rojo")
print(Back.WHITE+"Texto color rojo sobre fondo blanco")
print(Back.WHITE+Style.BRIGHT+"Txt rojo brill.s/blanco"+Back.RESET)
print(Style.RESET_ALL + "Texto con valores por defecto")
print(Fore.WHITE+Back.BLUE+"Texto blanco sobre azul"+Back.RESET)
print("Texto blanco sobre fondo negro")

# Niveles de intensidad

print(Style.DIM + Fore.WHITE + "Intensidad baja")
print(Style.NORMAL + "Intensidad normal")
print(Style.BRIGHT + "Intensidad alta")

# Obtener una lista de todos los exchanges disponibles en ccxt
exchanges = ccxt.exchanges

# Mostrar los nombres de los exchanges
print("Exchanges disponibles en ccxt:")
for exchange in exchanges:
    print(exchange)
"""


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