from dataclasses import dataclass, field

from gamenacki.common.card_pile import CardPile
from gamenacki.forbiddenislandnacki.models.flood_cards import FloodCard
from gamenacki.forbiddenislandnacki.models.treasure_cards import TreasureCard, create_treasure_cards
from gamenacki.forbiddenislandnacki.models.tiles import TILES


@dataclass
class Piles:
    treasure_cards: CardPile[TreasureCard] = field(default_factory=lambda: CardPile(create_treasure_cards(), True))
    treasure_card_discard: CardPile[TreasureCard] = field(default_factory=lambda: CardPile())
    flood_cards: CardPile[FloodCard] = field(default_factory=lambda: CardPile([FloodCard(t.name, t.img) for t in TILES]))
    flood_card_discard: CardPile[FloodCard] = field(default_factory=lambda: CardPile())

