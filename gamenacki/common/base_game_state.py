from abc import ABC, abstractmethod
from dataclasses import dataclass

from gamenacki.common.stack import Stack

@dataclass
class BaseGameState(ABC):
    player_cnt: int
    piles: "Piles"
    scorer: "Scorer"
    dealer: "Dealer"

    @abstractmethod
    def __post_init__(self):
        """create piles, create Dealer
        __post_init__(self):
            self.create_piles()
            self.deal()
        """

    @abstractmethod
    def create_piles(self) -> list[Stack]:
        ...

    @abstractmethod
    def deal(self) -> None:
        ...

    @property
    @abstractmethod
    def has_game_started(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_round_over(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_game_over(self) -> bool:
        ...

    @property
    def winner(self) -> None | tuple[int, int] | list[tuple[int, int]]:
        """Returns None if game not over; tuple[player_idx, points] if solo winner else list[tuple[]] for ties"""
        if not self.is_game_over:
            return None
        return self.scorer.get_winner(self.is_game_over)