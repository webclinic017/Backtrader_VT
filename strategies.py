import datetime
import backtrader as bt


class AsianKillZone(bt.Strategy):
    def log(self, txt, dt=None):
        dt = self.datas[0].datetime.datetime()
        print(f"{dt} {txt}")  # Print date and close

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.currDate = self.datas[0].datetime.date(0)
        self.currHigh = self.datas[0].high
        self.currLow = self.datas[0].low
        self.dailyHigh = self.currHigh[0]
        self.dailyLow = self.currLow[0]

        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            self.log(f"ORDER SUBMITTED, {order.executed.price:.6f}")
            # An active Buy/Sell order has been submitted/accepted - Nothing to do
            return
        if order.status in [order.Submitted]:

            # An active Buy/Sell order has been submitted/accepted - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED, {order.executed.price:.6f}")
            elif order.issell():
                self.log(f"SELL EXECUTED, {order.executed.price:.6f}")
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        # Reset orders
        self.order = None

    def next(self):
        if self.data.datetime.time() == datetime.time(0, 0):
            self.dailyHigh = self.currHigh[0]
            self.dailyLow = self.currLow[0]
        if self.datas[0].datetime.time() < datetime.time(7, 0) and self.datas[
            0
        ].datetime.time() >= datetime.time(
            0, 0
        ):  # Asian range
            self.dailyHigh = max(self.currHigh[0], self.dailyHigh)
            self.dailyLow = min(self.currLow[0], self.dailyLow)

        # Check for open orders
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            self.order = self.sell(
                exectype=bt.Order.Limit,
                price=self.dailyHigh,
                valid=datetime.datetime.now() + datetime.timedelta(days=1),
            )

        else:
            # We are already in the market, look for a signal to CLOSE trades
            if self.currLow[0] < self.dailyLow:
                self.log(f"CLOSE CREATE {self.dataclose[0]:6f}")
                self.order = self.close()
