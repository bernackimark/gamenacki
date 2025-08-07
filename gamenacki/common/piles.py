"""A module for general subclassers of cardnacki.pile.Pile ... not sure how valuable this is;
The concept is that defining the Piles (core to most games) here will reduce the size of the GameState constructor"""

from dataclasses import dataclass

from cardnacki.pile import Pile


@dataclass
class Hand(Pile):
    ...


@dataclass
class Discard(Pile):
    ...
