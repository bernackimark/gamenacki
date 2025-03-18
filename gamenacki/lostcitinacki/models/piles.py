"""A module for collections of cards"""

from dataclasses import dataclass, field
from itertools import product

import gamenacki.common.piles
from gamenacki.common.piles import CardStack, BaseDeck, Discard, Hand
from gamenacki.lostcitinacki.models.cards import Card, Handshake, ExpeditionCard
from gamenacki.lostcitinacki.models.constants import Color, DrawFromStack, PlayToStack


@dataclass
class Expedition(CardStack):
    color: Color = None

    def __post_init__(self):
        if not self.color:
            raise ValueError("Color must be provided")

    def __repr__(self) -> str:
        return f'{self.color.value} {self.cards}'

    @property
    def card_cnt(self) -> int:
        return len(self)

    @property
    def handshake_cnt(self) -> int:
        return sum([1 for c in self if isinstance(c, Handshake)])

    @property
    def points(self) -> int:
        if not self.card_cnt:
            return 0
        plus_minus = sum([c.value for c in self]) - 20
        multiplier = 1 + self.handshake_cnt
        bonus = 20 if self.card_cnt >= 8 else 0
        return plus_minus * multiplier + bonus


def create_board() -> list[Expedition]:
    return [Expedition([], c) for c in list(Color)]


@dataclass
class ExpeditionBoard:
    """One ExpeditionBoard is given to each play; it's a collection of color expeditions"""
    expeditions: list[Expedition] = field(default_factory=create_board)

    def __repr__(self) -> str:
        return 'Expeditions: ' + ' '.join([ep.__repr__() for ep in self.expeditions])

    def __iter__(self):
        return iter(self.expeditions)

    @property
    def points(self) -> int:
        return sum([p.points for p in self.expeditions])

    def get_max_card_in_color(self, color: Color) -> int:
        numbered_cards = [c.value for p in self for c in p if p.color == color and isinstance(c, ExpeditionCard)]
        return max(numbered_cards) if numbered_cards else 0

    def clear(self) -> None:
        [pile.clear() for pile in self.expeditions]


@dataclass
class Hand(gamenacki.common.piles.Hand):
    def get_possible_moves(self, board_playable_cards: list[Card],
                           discard_has_cards: bool) -> list[tuple[Card, PlayToStack, DrawFromStack]]:
        """Return combos of (card, DISCARD/EXPEDITION, DECK/DISCARD) where allowed by game rules"""
        possible_moves: list[tuple[Card, PlayToStack, DrawFromStack]] = []
        for card, play_to_stack, draw_from_stack in product(self.cards, set(PlayToStack), set(DrawFromStack)):
            if (play_to_stack == PlayToStack.DISCARD and draw_from_stack == DrawFromStack.DECK) or \
                (play_to_stack == PlayToStack.EXPEDITION and card in board_playable_cards and
                (draw_from_stack == DrawFromStack.DECK or (draw_from_stack == DrawFromStack.DISCARD and discard_has_cards))):
                possible_moves.append((card, play_to_stack, draw_from_stack))

        print(possible_moves)

        return possible_moves

@dataclass
class Deck(BaseDeck):
    @staticmethod
    def build_deck() -> list[Card]:
        handshakes: list[Handshake] = [Handshake(c) for c in list(Color) for _ in range(3)]
        expeditions: list[ExpeditionCard] = [ExpeditionCard(c, v) for c in list(Color) for v in range(6, 11)]
        return handshakes + expeditions


@dataclass
class Piles:
    """deck & discard are being populated here; hands & exp boards are populated elsewhere as they are 1 per player"""
    hands: list[Hand] = field(default_factory=list)
    deck: Deck = field(default_factory=Deck)
    discard: Discard = field(default_factory=Discard)
    exp_boards: list[ExpeditionBoard] = field(default_factory=list)
