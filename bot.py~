import pandas as pd
import time
from yahoo_fin import stock_info as si

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from stockReport import sentiments
from strats import *

API_KEY = 'PKA6KC6N672RZ773ZXRB'
SECRET_KEY = 'eElymeK26x5bKKn5yuPmUZz2SOXVLeg14LEnLLo2'

client = TradingClient(API_KEY, SECRET_KEY, paper=True)

df = pd.DataFrame(si.tickers_sp500())
symbols = set(symbol for symbol in df[0].values.tolist())

cash = 1000

while True:
    results = sentiments(symbols, progress=True)
    ordSents = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    for stockName in list(ordSents)[:20]:
        print(f'Buying ${cash} of {stockName}')
        stopLoss(client, stockName, cash, stop=0.95, take=1.05)

    time.sleep(15*60)
