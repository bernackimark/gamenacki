"""A module for common game collections such as Deck (an ABC), Hand, Discard. All subclass CardStack (a child of Stack).
CardStack allows its implementers to use the attribute 'cards' instead of 'items'"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random

from gamenacki.common.stack import Stack
from gamenacki.lostcitinacki.models.cards import Card


@dataclass
class CardStack(Stack, ABC):
    """This subclass' purpose is to have callers/subclassers use the attribute 'cards' instead of the generic 'items'.
    If something subclasses CardStack & wants to initialize with cards, it will still need to use '_items --
     ex: _items: list[Card] = field(default_factory=build_deck)"""
    _items: list[Card] = field(default_factory=list)

    @property
    def cards(self) -> list:
        return self._items

    @cards.setter
    def cards(self, value: list):
        if not isinstance(value, list):
            raise ValueError("cards must be a list")
        for item in value:
            self.push(item)  # Ensure each item is of type Card when setting cards
        self._items = value


@dataclass
class BaseDeck(CardStack, ABC):
    _items: list[Card] = field(default_factory=list)
    start_shuffled: bool = True

    def __post_init__(self):
        self._items = self.build_deck()
        if self.start_shuffled:
            random.shuffle(self._items)

    @staticmethod
    @abstractmethod
    def build_deck() -> list[Card]:
        ...


@dataclass
class Hand(CardStack):
    ...


@dataclass
class Discard(CardStack):
    ...
