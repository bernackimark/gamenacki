import random
from dataclasses import dataclass, field

from gamenacki.forbiddenislandnacki.models.flood_cards import FloodCard
from gamenacki.forbiddenislandnacki.models.treasure_cards import TreasureCard, create_treasure_cards
from gamenacki.forbiddenislandnacki.models.tiles import TILES


@dataclass
class TreasureCardPile:
    cards: list[TreasureCard] = field(default_factory=create_treasure_cards)

    def __post_init__(self):
        random.shuffle(self.cards)


@dataclass
class TreasureDiscardPile:
    cards: list[TreasureCard] = field(default_factory=list)


@dataclass
class FloodCardPile:
    cards: list[FloodCard] = field(default_factory=lambda: [FloodCard(t.name, t.img) for t in TILES])

    def __post_init__(self):
        random.shuffle(self.cards)


@dataclass
class FloodDiscardPile:
    cards: list[FloodCard] = field(default_factory=list)


@dataclass
class Piles:
    treasure_cards: TreasureCardPile = field(default_factory=TreasureCardPile)
    treasure_card_discard: TreasureDiscardPile = field(default_factory=TreasureDiscardPile)
    flood_cards: FloodCardPile = field(default_factory=FloodCardPile)
    flood_card_discard: FloodDiscardPile = field(default_factory=FloodDiscardPile)

