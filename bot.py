import pandas as pd
import time
from yahoo_fin import stock_info as si

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import alpaca_trade_api as tradeapi

from stockReport import sentiments
from strats import *

API_KEY = 'PKA6KC6N672RZ773ZXRB'
SECRET_KEY = 'eElymeK26x5bKKn5yuPmUZz2SOXVLeg14LEnLLo2'

client = TradingClient(API_KEY, SECRET_KEY, paper=True)

df = pd.DataFrame(si.tickers_sp500())
symbols = set(symbol for symbol in df[0].values.tolist())

cash = 100000
investMinutes = 15
investPercent = 0.2

longNum = 10
shortNum = 10

while True:
    results = sentiments(symbols, progress=True)
    ordSents = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    investCash = (cash * investPercent) // (longNum + shortNum)

    # long
    for stockName in list(ordSents)[:longNum]:
        print(f'Buying ${cash} of {stockName}')
        stopLoss(client, stockName, investCash, stop=0.95, take=1.05)

    # short
    for stockName in list(ordSents)[-shortNum:]:
        print(f'Buying ${cash} of {stockName}')
        stopLoss(client, stockName, investCash, buy=False, stop=1.05, take=0.95)

    cash -= investCash * (longNum + shortNum)
    time.sleep(investMinutes*60)

