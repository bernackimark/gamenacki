"""A module for collections of cards"""

from dataclasses import dataclass, field

from cardnacki.pile import Deck
from gamenacki.common.piles import Hand


@dataclass
class Piles:
    hand: Hand = field(default_factory=Hand)
    deck: Deck = field(default_factory=lambda: Deck(True))

