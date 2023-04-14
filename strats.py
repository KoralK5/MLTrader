from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import numpy as np

import requests
from bs4 import BeautifulSoup

def ceil(a, precision=0):
    return np.true_divide(np.ceil(a * 10**precision), 10**precision)

def floor(a, precision=0):
    return np.true_divide(np.floor(a * 10**precision), 10**precision)

def getPrice(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    current_price_tag = soup.find("fin-streamer", {"data-test": "qsp-price"})
    current_price = float(current_price_tag["value"])
    return current_price

def stopLoss(client, symbol, cash, buy=True, stop=0.95, take=1.05):
    symbol_price = getPrice(symbol)
    stop_loss = floor(symbol_price * stop, 2) if buy else ceil(symbol_price * stop, 2)
    take_profit = ceil(symbol_price * take, 2) if buy else floor(symbol_price * take, 2)

    client.submit_order(order_data=MarketOrderRequest(
        symbol=symbol,
        qty=cash//symbol_price,
        side='buy' if buy else 'sell',
        type='market',
        time_in_force='day',
        order_class='bracket',
        stop_loss={'stop_price': stop_loss},
        take_profit={'limit_price': take_profit}
    ))
