import random
from dataclasses import dataclass, field
from typing import TypeVar, Generic

T = TypeVar("T")  # Generic type for items


@dataclass
class CardPile(Generic[T]):
    """A general collection that accepts a list of items to: pop, push, shuffle, peek, remove, clear.
    Push requires the items to be of a Generic TypeVar"""
    cards: list[T] = field(default_factory=list)
    start_shuffled: bool = False

    def __post_init__(self):
        if not self.cards:
            self.cards = []
        if self.start_shuffled:
            self.shuffle()

    def __iter__(self):
        return iter(self.cards)

    def __len__(self) -> int:
        return len(self.cards) if self.cards else 0

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def push(self, card: T) -> None:
        self.cards.append(card)

    def remove(self, card: T) -> None:
        if card not in self.cards:
            raise ValueError(f"{card} not found")
        self.cards.remove(card)

    def pop(self) -> T | None:
        return self.cards.pop() if self.cards else None

    def clear(self) -> None:
        self.cards.clear()

    def peek(self) -> T | None:
        return self.cards[-1] if self.cards else None

    def reveal(self) -> list[T]:
        return self.cards
