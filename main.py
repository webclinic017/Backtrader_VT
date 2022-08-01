import backtrader as bt
import datetime
from strategies import *
import pandas as pd

# dataframe = pd.read_csv("GOOGL_15.csv")

# Instantiate Cerebro engine
cerebro = bt.Cerebro()

# Add data feed to Cerebro
data = bt.feeds.GenericCSVData(
    dataname="FX_GBPUSD, 5.csv",
    dtformat=("%Y-%m-%dT%H:%M:%SZ"),
    timeframe=bt.TimeFrame.Minutes,
    compression=60,
    datetime=0,
    high=2,
    low=3,
    open=1,
    close=4,
    volume=-1,
    openinterest=-1,
)
cerebro.adddata(data)

# Add strategy to Cerebro
cerebro.addstrategy(AsianKillZone)

# Default position size
cerebro.addsizer(bt.sizers.SizerFix, stake=100)

if __name__ == "__main__":
    start_portfolio_value = cerebro.broker.getvalue()
    print(f"Starting Portfolio Value: {start_portfolio_value:2f}")

    # Run Cerebro Engine
    cerebro.run()

    # .getvalue() obtains value of portfolio at any time
    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    print(f"Final Portfolio Value: {end_portfolio_value:2f}")
    print(f"PnL: {pnl:.2f}")
