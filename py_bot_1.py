import asyncio
import os
from random import randint
import sys
import traceback

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt  # noqa: E402

exchanges = [
    ccxt.okx(),
    ccxt.bybit({"options":{"defaultType":"spot"}}),
    ccxt.binance(),
    ccxt.kucoin(),
    ccxt.bitmart(),
    ccxt.gate()
]

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
    #async with aiohttp.ClientSession() as session:
    prices = await get_last_prices()
    for symbol in symbols:
        print (symbol)
    #await session.close()

async def main():
        
    try:
        print ("*******************")
        await bot()
        print ("fin")
    
    except Exception as e:
        print(f'Fallado con: {e}')
        print(traceback.format_exc())

asyncio.run(main())
