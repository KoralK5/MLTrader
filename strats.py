from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

import requests
from bs4 import BeautifulSoup

def getPrice(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    current_price_tag = soup.find("fin-streamer", {"data-test": "qsp-price"})
    current_price = float(current_price_tag["value"])
    return current_price

def stopLoss(client, symbol, cash, buy=True, stop=0.95, take=1.05):
    symbol_price = getPrice(symbol)
    stop_loss = min(symbol_price * stop, symbol_price - 0.01) if buy else max(symbol_price * stop, symbol_price + 0.01)
    take_profit = max(symbol_price * take, symbol_price + 0.01) if buy else min(symbol_price * take, symbol_price - 0.01)

    try:
        client.submit_order(order_data=MarketOrderRequest(
            symbol=symbol,
            qty=cash//symbol_price,
            side='buy' if buy else 'sell',
            type='market',
            time_in_force='day',
            order_class='bracket',
            stop_loss={'stop_price': round(stop_loss, 2)},
            take_profit={'limit_price': round(take_profit, 2)}
        ))
    except:
        return
