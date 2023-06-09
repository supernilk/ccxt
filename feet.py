import ccxt

exchange = ccxt.binance({
    'apiKey': 'XYkJv3qaLJWkeDY3U4fgDePTLgum3xqXqC7zBrHJiPqWekLWhr99nzRhCX7r9o56',
    'secret': 'k5SXn6NWYyeBPsqejBPkg6JWu1kDSiayVlaPUrS9GUS2R4Pz5imx9fP1xqrlolQu',
})

exchange = ccxt.binance()
fees = exchange.fetch_trading_fees()
a= exchange.fetch_tr

print(fees)