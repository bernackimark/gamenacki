from abc import ABC, abstractmethod
from dataclasses import dataclass
import random
import time

from gamenacki.lostcitinacki.models.cards import Card
from gamenacki.lostcitinacki.models.constants import DrawFromStack, PlayToStack
from gamenacki.common.piles import Hand


@dataclass
class Player(ABC):
    idx: int
    name: str

    @abstractmethod
    def play_card(self, h: Hand, board_playable_cards: list[Card]) -> tuple[Card, PlayToStack]:
        ...

    def pick_up_from(self, can_pick_up_discard: bool, is_discard_card_playable: bool) -> DrawFromStack:
        """Method that applies to all children and ensures this check runs first
        If player cannot pick up from discard, Deck is returned without yielding to child method
        Else, child may pick up from Deck or Discard; Bot will pick from Deck if top discard is not playable"""
        if not can_pick_up_discard:
            return DrawFromStack.DECK
        return self._child_pick_up_from(is_discard_card_playable)

    @abstractmethod
    def _child_pick_up_from(self, is_discard_card_playable: bool) -> DrawFromStack:
        ...


@dataclass
class ConsolePlayer(Player):
    def play_card(self, h: Hand, board_playable_cards: list[Card]) -> tuple[Card, PlayToStack]:
        card, exp_or_discard = None, None
        while card is None:
            sel_card = input('Select a card to play: ')
            card = next((c for c in h if c.__repr__() == sel_card), None)
        while exp_or_discard not in ('e', 'd'):
            exp_or_discard = input('Play to expedition or discard (e/d): ')
        return card, PlayToStack.EXPEDITION if exp_or_discard == 'e' else PlayToStack.DISCARD

    def _child_pick_up_from(self, is_discard_card_playable: bool) -> DrawFromStack:
        value, allowed_values = None, ('de', 'di')
        while value not in allowed_values:
            value = input('Pick up from deck or discard (de/di): ')
        return DrawFromStack.DECK if value == 'de' else DrawFromStack.DISCARD

@dataclass
class BotPlayer(Player):
    def play_card(self, h: Hand, board_playable_cards: list[Card]) -> tuple[Card, PlayToStack]:
        playable_cards = [card for card in h.cards if card in board_playable_cards]
        if not playable_cards:
            return random.choice(h.cards), PlayToStack.DISCARD
        return random.choice(playable_cards), PlayToStack.EXPEDITION

    def _child_pick_up_from(self, is_discard_card_playable: bool) -> DrawFromStack:
        time.sleep(0.5)
        if not is_discard_card_playable:
            return DrawFromStack.DECK
        return DrawFromStack.DECK if random.randint(1, 10) > 8 else DrawFromStack.DISCARD
