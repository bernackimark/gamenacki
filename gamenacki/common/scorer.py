"""BaseGameState creates an instance of Scorer as an attribute"""

from dataclasses import dataclass, field
from enum import Enum, auto


@dataclass
class Ledger:
    ledger: list[int] = field(default_factory=list)

    def add_a_value(self, score: int) -> None:
        if not isinstance(score, int):
            raise ValueError(f"{score} must be an integer")
        self.ledger.append(score)

    @property
    def total(self) -> int:
        return sum(self.ledger) if self.ledger else 0


class WinCondition(Enum):
    HIGHEST_SINGLE_SCORE = auto()
    HIGHEST_SCORE_W_TIES = auto()
    LOWEST_SINGLE_SCORE_UPPER_BOUND_REACHED = auto()
    LOWEST_SCORE_W_TIES_UPPER_BOUND_REACHED = auto()


@dataclass
class Scorer:
    """Maintains ledgers, a win condition, the target score, who won ..."""
    ledgers: list[Ledger]
    win_condition: WinCondition
    target_score: int = None

    @property
    def p_idx_points(self) -> list[tuple[int, int]]:
        return [(i, pl.total) for i, pl in enumerate(self.ledgers)]

    @property
    def max_points(self) -> int:
        return max(t[1] for t in self.p_idx_points)

    @property
    def min_points(self) -> int:
        return min(t[1] for t in self.p_idx_points)

    @property
    def max_points_players(self) -> list[tuple[int, int]]:
        return [e for e in self.p_idx_points if e[1] == self.max_points]

    @property
    def min_points_players(self) -> list[tuple[int, int]]:
        return [e for e in self.p_idx_points if e[1] == self.min_points]

    def get_winner(self, is_game_over: bool, *args) -> None | tuple[int, int] | list[tuple[int, int]]:
        if not is_game_over or (self.target_score and self.max_points < self.target_score):
            return None

        if self.win_condition == WinCondition.HIGHEST_SINGLE_SCORE:
            winners = self.max_points_players
            return winners[0] if len(winners) == 1 else None
        elif self.win_condition == WinCondition.HIGHEST_SCORE_W_TIES:
            winners = self.max_points_players
            return winners[0] if len(winners) == 1 else winners
        elif self.win_condition == WinCondition.LOWEST_SINGLE_SCORE_UPPER_BOUND_REACHED:
            winners = self.min_points_players
            return winners[0] if len(winners) == 1 else None
        elif self.win_condition == WinCondition.LOWEST_SCORE_W_TIES_UPPER_BOUND_REACHED:
            winners = self.min_points_players
            return winners[0] if len(winners) == 1 else winners
        else:
            raise ValueError("Unknown Win Condition")
