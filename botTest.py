from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
from pandas_ta import rsi

class Bot(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)
        # self.rsi = self.I(rsi, self.data.df.Close, length=14)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()

backtest = Backtest(GOOG, Bot, cash=1000, commission=0.002, exclusive_orders=True)
stats = backtest.run()

print(stats)

# backtest.plot()
