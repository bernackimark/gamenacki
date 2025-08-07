"""Contains enums"""

from enum import auto

from cardnacki.constants import PokerHand
from gamenacki.common.base_constants import BaseAction

class Action(BaseAction):
    BEGIN_GAME = auto()
    BEGIN_ROUND = auto()
    DRAW = auto()
    END_ROUND = auto()
    END_GAME = auto()


PRIZE_TABLE = {PokerHand.ROYAL_FLUSH: 976, PokerHand.STRAIGHT_FLUSH: 50, PokerHand.FOUR_OF_A_KIND: 25,
               PokerHand.FULL_HOUSE: 9, PokerHand.FLUSH: 6, PokerHand.STRAIGHT: 4, PokerHand.THREE_OF_A_KIND: 3,
               PokerHand.TWO_PAIR: 2, PokerHand.JACKS_OR_BETTER: 1}

# runs all 2,598,960 five-card hands, find the frequency and prize sums for each possible outcome
NO_DRAW_LIKELIHOOD = {PokerHand.ROYAL_FLUSH: (1.5390771693292702e-06, 0.0015021393172653676),
                      PokerHand.STRAIGHT_FLUSH: (1.3851694523963431e-05, 0.0006925847261981716),
                      PokerHand.FOUR_OF_A_KIND: (0.00024009603841536616, 0.006002400960384154),
                      PokerHand.FULL_HOUSE: (0.0014405762304921968, 0.012965186074429771),
                      PokerHand.FLUSH: (0.001965401545233478, 0.011792409271400867),
                      PokerHand.STRAIGHT: (0.003924646781789639, 0.015698587127158554),
                      PokerHand.THREE_OF_A_KIND: (0.02112845138055222, 0.06338535414165666),
                      PokerHand.TWO_PAIR: (0.0475390156062425, 0.095078031212485),
                      PokerHand.JACKS_OR_BETTER: (0.13002123926493675, 0.13002123926493675)}
