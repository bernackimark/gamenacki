"""A module for general subclassers of cardnacki.pile.Pile ... not sure how valuable this is"""

from dataclasses import dataclass

from cardnacki.pile import Pile


@dataclass
class Hand(Pile):
    ...


@dataclass
class Discard(Pile):
    ...
