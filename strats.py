from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

def stopLoss(client, symbol, cash, stop=0.95, take=1.05):
    symbol_bars = api.get_barset(symbol, 'minute', 1).df.iloc[0]
    symbol_price = symbol_bars[symbol]['close']

    client.submit_order(order_data=MarketOrderRequest(
                        symbol=symbol,
                        qty=cash//symbol_price,
                        side=OrderSide.SELL,
                        time_in_force=TimeInForce.DAY,
                        order_class='oco',
                        stop_loss={'stop_price': symbol_price * stop},
                        take_profit={'limit_price': symbol_price * take}
                        ))
