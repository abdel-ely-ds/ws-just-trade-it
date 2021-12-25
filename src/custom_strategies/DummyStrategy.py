from numpy.random import choice
from t_nachine.backtester import Strategy
from t_nachine.candlesticks import Candle
from t_nachine.risk import RiskManger
from t_nachine.strategies.utils import add_attrs, get_candles, build_attr_dict

WAIT = 1  # cancel pending orders after 1 day
P_BUY = 0.1  # probability to buy

RISK_PER_TRADE = 0.01
RISK_TO_REWARD = 2.0


class DummyStrategy(Strategy):
    def init(self):

        # Risk manager
        self.wait = WAIT
        self.p_buy = P_BUY
        self.risk_to_reward = RISK_TO_REWARD
        self.risk_per_trade = RISK_PER_TRADE
        self.risk_manager = RiskManger(
            risk_to_reward=self.risk_to_reward, risk_per_trade=self.risk_per_trade
        )

    def cancel(self) -> None:
        """
        wait until <self.wait> days then cancel order if not executed
        """
        for order in self.orders:
            if (
                    not order.is_contingent
                    and len(self.data) - order.placed_bar >= self.wait
            ):
                order.cancel()

    def buy_signal(self, candle0: Candle, candle1: Candle) -> bool:

        return candle1.low < candle0.high and choice(["buy", "sell"], 1, p=[self.p_buy, 1 - self.p_buy]) == "buy"

    def next(self):
        # cancel pending orders
        self.cancel()
        # add attributes
        for trade in self.trades:
            add_attrs(
                trade=trade,
                high=self.data.High[-1],
                low=self.data.Low[-1],
                **build_attr_dict(self.data),
            )

        candle0, candle1 = get_candles(self.data, days=2)  # today and yesterday candle
        if self.buy_signal(candle0, candle1):
            # entries and exits and number of shares
            stop, limit, sl, tp = self.risk_manager.compute_entry_exit(
                above_price=candle0.high, below_price=candle1.low
            )
            size = self.risk_manager.shares(self.equity, stop, sl)
            order = self.buy(stop=stop, limit=limit, sl=sl, tp=tp, size=size)
            setattr(order, "placed_bar", len(self.data))
