# -*- coding: utf-8 -*-
# https://github.com/ccxt/ccxt/blob/master/examples/bots/py/spot-arbitrage-bot.py
import asyncio
import os
from random import randint
import sys
from pprint import pprint
import time
from time import gmtime, strftime
import traceback


root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt  # noqa: E402

print('CCXT Version:', ccxt.__version__)

####################################################################################
# Simple arbitrage bot that will look for arbitrage opportunities on spot markets ##
# and execute them using market orders.                                           ##
#                                                                                 ##                 
# Disclaimer: this bot is for educational purposes only. Use at your own risk.    ##
####################################################################################

########################## Requerimientos ##########################################
# pyenv local 3.8.8
# python -m venv venv
# .\venv\Scripts\activate
# Linux: source venv/bin/activate
# pip freeze


# bot options
wait_time = 5 # seconds to wait between each check
paper_trading = True # set to false to actually execute trades

# exchanges you want to use to look for arbitrage opportunities
exchanges = [
    ccxt.okx(),
    ccxt.bybit({"options":{"defaultType":"spot"}}),
    ccxt.binance(),
    ccxt.kucoin(),
    ccxt.bitmart(),
    ccxt.gate()
]

# symbols you want to trade
symbols = [
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

# order sizes for each symbol, adjust it to your liking
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
    tasks = [ exchange.fetch_tickers(symbols) for exchange in exchanges ]
    results = await asyncio.gather(*tasks)
    
    for exchange in exchanges:
        await exchange.close()
    
    return results

async def bot():
    prices = await get_last_prices()
    for symbol in symbols:
        ms = int(time.time() * 1000)
        mss = strftime("%d %b %Y %H:%M:%S ", gmtime())

        symbol_prices = [ exchange_prices[symbol]['last'] for exchange_prices in prices ]

        min_price = min(symbol_prices)
        max_price = max(symbol_prices)

        order_size = order_sizes[symbol]

        min_exchange = exchanges[symbol_prices.index(min_price)]
        max_exchange = exchanges[symbol_prices.index(max_price)]

        # calculate min exchange taker fee
        # warning: you need to manually check if there are special campaign fees 
        min_exchange_fee = min_exchange.fees['trading']['taker']

        min_fee = order_size * min_price * min_exchange_fee

        # calculate max exchange taker fee
        # warning: you need to manually check if there are special campaign fees 
        max_exchange_fee = max_exchange.fees['trading']['taker']
        max_fee = order_size * max_price * max_exchange_fee

        price_profit = max_price - min_price
        profit = (price_profit * order_size) - (min_fee) - (max_fee)

        if (profit > 0): # not taking into account slippage or order book depth
            print(ms, symbol, "profit:", profit, "Buy", min_exchange.id, min_price, "Sell", max_exchange.id, max_price)
        
            if not paper_trading:
                    buy_min = min_exchange.create_market_buy_order(symbol, order_size)
                    sell_max = max_exchange.create_market_sell_order(symbol, order_size)
                    orders = await asyncio.gather(buy_min, sell_max) # se ejecutan simultáneamente
                    print("Órdenes ejecutadas con éxito")
        else:
            print(str(mss), symbol, "sin oportunidad de arbitraje")

async def check_requirements():
    try:
        print("Comprobando si los intercambios admiten fetchTickers y los símbolos que queremos intercambiar")

        for exchange in exchanges:
            pprint (exchange)
            if not exchange.has['fetchTickers']:
                print(exchange.id, "no es compatible con fetchTickers")

            await exchange.load_markets()
            
            for symbol in symbols:
                if symbol not in exchange.markets:
                    print (symbol,"..........[Error!]")        
                else:
                    print (symbol,"..............[ok]")


    except Exception as e:
        print(f'Fallado con: {e}')

async def main():
    #await check_requirements()
    print("Despertando el Bot")
    
    #while True:
        
    try:
        print ("*******************")
        await bot()

        print ("fin")
    
    except Exception as e:
        print(f'Fallado con: {e}')
        print(traceback.format_exc())

asyncio.run(main())
