from collections import OrderedDict
from typing import List

import numpy as np
from t_nachine.backtester import Strategy
from t_nachine.candlesticks import Candle
from t_nachine.indicators import ema
from t_nachine.patterns import AnyReversalPattern
from t_nachine.risk import RiskManger
from t_nachine.strategies.utils import add_attrs, build_attr_dict, get_candles

UP_DAYS = 20
WAIT = 1
RISK_PER_TRADE = 0.01
RISK_TO_REWARD = 2.0


class DummyStrategy(Strategy):
    def init(self):
        # data and indicators
        self.ema18 = self.I(ema, self.data, 18)
        self.ema50 = self.I(ema, self.data, 50)
        self.ema100 = self.I(ema, self.data, 100)
        self.ema150 = self.I(ema, self.data, 150)
        self.ema200 = self.I(ema, self.data, 200, color="red")
        self.up_days = UP_DAYS
        self.wait = WAIT
        self.risk_to_reward = RISK_TO_REWARD
        self.risk_per_trade = RISK_PER_TRADE
        self.risk_manager = RiskManger(
            risk_to_reward=self.risk_to_reward, risk_per_trade=self.risk_per_trade
        )

    def cancel(
        self,
    ) -> None:
        """
        wait until <self.wait> days then cancel order if not executed
        """
        for order in self.orders:
            if (
                not order.is_contingent
                and len(self.data) - order.placed_bar >= self.wait
            ):
                order.cancel()

    def uptrend(self) -> bool:
        """
        checks if the trend is bullish

        Returns:
            bool: if is uptrend
        """
        ema50_above_ema100_above_ema200: bool = all(
            [
                self.ema50[i] >= self.ema100[i] >= self.ema200[i]
                for i in range(-self.up_days, -1)
            ]
        )
        ema18_above_ema50 = np.mean(
            [self.ema18[i] >= self.ema50[i] for i in range(-int(self.up_days / 2), -3)]
        ) >= 0.9 and all([self.ema18[i] > self.ema50[i] for i in range(-3, 0)])

        return ema18_above_ema50 and ema50_above_ema100_above_ema200

    @staticmethod
    def confirmed(candle0: Candle, candle1: Candle) -> bool:
        """
        check if the reversal candle is confirmed

        Args:
            candle0 (Candle): today's candle
            candle1 (Candle): yesterday's candle

        Returns:
            [bool]: true if confirmed
        """
        return (
            candle0.low > candle1.low
            and candle0.close > candle1.high
            and candle0.bull()
        )

    def buy_signal(
        self, candle0: Candle, candle1: Candle, candle2: Candle, support: List[float]
    ) -> bool:
        """
        buy signal

        Args:
            candle0 (Candle): [description]
            candle1 ([type]): [description]
            candle2 (Candle): [description]
            support (List[float]): [description]

        Returns:
            bool: is buy signal triggered
        """

        is_reversal = AnyReversalPattern(
            candle=candle1, pre_candle=candle2, support=support
        )
        is_uptrend = self.uptrend()
        is_confirmed = self.confirmed(candle0, candle1)

        return is_uptrend and is_confirmed and is_reversal

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

        try:
            supports = OrderedDict(
                [
                    (200, [self.ema200[-1], self.ema200[-2], self.ema200[-3]]),
                    (150, [self.ema150[-1], self.ema150[-2], self.ema150[-3]]),
                    (100, [self.ema100[-1], self.ema100[-2], self.ema100[-3]]),
                    (50, [self.ema50[-1], self.ema50[-2], self.ema50[-3]]),
                ]
            )

            (
                candle0,
                candle1,
                candle2,
            ) = get_candles(self.data, days=3)

            for support in supports.values():

                if self.buy_signal(candle0, candle1, candle2, support):
                    # entries and exits and number of shares
                    stop, limit, sl, tp = self.risk_manager.compute_entry_exit(
                        above_price=candle0.high, below_price=candle1.low
                    )
                    size = self.risk_manager.shares(self.equity, stop, sl)
                    order = self.buy(stop=stop, limit=limit, sl=sl, tp=tp, size=size)
                    setattr(order, "placed_time", self.data.index[-1])
                    setattr(order, "placed_bar", len(self.data))
        except IndexError:
            pass

