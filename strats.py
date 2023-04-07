from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import alpaca_trade_api as tradeapi

import requests
from bs4 import BeautifulSoup

def getPrice(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    current_price_tag = soup.find("fin-streamer", {"data-test": "qsp-price"})
    current_price = float(current_price_tag["value"])
    return current_price

def stopLoss(client, symbol, cash, stop=0.95, take=1.05):
    symbol_price = getPrice(symbol)

    client.submit_order(order_data=MarketOrderRequest(
        symbol=symbol,
        qty=cash/symbol_price,
        side='buy',
        type='market',
        time_in_force='day',
        order_class='bracket',
        stop_loss={'stop_price': symbol_price * stop},
        take_profit={'limit_price': symbol_price * take}
    ))
