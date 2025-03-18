import random
from dataclasses import dataclass, field
from typing import TypeVar, Generic

T = TypeVar("T")  # Generic type for stack items


@dataclass
class Stack(Generic[T]):
    """A general collection that accepts a list of items to: pop, push, shuffle, peek, remove, clear"""
    _items: list[T] = field(default_factory=list)

    def __post_init__(self):
        if not self._items:
            self._items = []

    def __iter__(self):
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items) if self._items else 0

    def shuffle(self):
        random.shuffle(self._items)

    def push(self, item: T):
        self._items.append(item)

    def remove(self, item: T):
        if item not in self._items:
            raise ValueError(f"{item} not found")
        self._items.remove(item)

    def pop(self) -> T | None:
        return self._items.pop() if self._items else None

    def clear(self) -> None:
        self._items.clear()

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

    def reveal(self) -> list[T]:
        return self._items
