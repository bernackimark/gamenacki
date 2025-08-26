from abc import ABC
from dataclasses import dataclass

from gamenacki.forbiddenislandnacki.models.treasures import TREASURES


@dataclass
class TreasureCard(ABC):
    name: str
    is_instant: bool
    action_text: str = None

    def __repr__(self) -> str:
        return self.name

@dataclass(repr=False)
class TreasureCardTreasure(TreasureCard):
    name: str
    is_instant: bool = False
    action_text: str = ''

@dataclass(repr=False)
class TreasureCardWatersRise(TreasureCard):
    name: str = 'Waters Rise!'
    is_instant: bool = False
    action_text: str = 'do the waters rise thing'

@dataclass(repr=False)
class TreasureCardHelicopterLift(TreasureCard):
    name: str = 'Helicopter Lift'
    is_instant: bool = True
    action_text: str = 'use at any time, fly some people on the same tile to any other tile'

@dataclass(repr=False)
class TreasureCardSandbags(TreasureCard):
    name: str = 'Sandbags'
    is_instant: bool = True
    action_text: str = 'shore up any tile'


def create_treasure_cards() -> list[TreasureCard]:
    treasures: list[TreasureCardTreasure] = [TreasureCardTreasure(t.value) for t in TREASURES for _ in range(5)]
    waters_rise: list[TreasureCard] = [TreasureCardWatersRise() for _ in range(3)]
    helicopter_lift: list[TreasureCard] = [TreasureCardHelicopterLift() for _ in range(3)]
    sandbags: list[TreasureCard] = [TreasureCardSandbags() for _ in range(2)]
    return treasures + waters_rise + helicopter_lift + sandbags
