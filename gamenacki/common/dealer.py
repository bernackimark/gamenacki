from dataclasses import dataclass
import random

from gamenacki.common.stack import Stack

@dataclass
class Dealer:
    """A grouping of commonly-used Dealer methods, such as dealing, tracking turns, current player, etc"""
    player_cnt: int
    dealer_idx: int = None
    player_turn_idx: int = None
    current_round_number = 1

    def __post_init__(self):
        self.dealer_idx = self.select_random_p_idx()
        self.advance_turn()

    def select_random_p_idx(self):
        return random.randint(0, self.player_cnt - 1)

    def advance_turn(self) -> None:
        self.player_turn_idx = (self.player_turn_idx + 1) % self.player_cnt if self.player_turn_idx is not None \
            else (self.dealer_idx + 1) % self.player_cnt

    def advance_button(self) -> None:
        self.dealer_idx = (self.dealer_idx + 1) % self.player_cnt

    def set_player_idx_as_left_of_dealer(self) -> None:
        """Must advance button first"""
        self.player_turn_idx = (self.dealer_idx + 1) % self.player_cnt

    def increment_round_number(self) -> None:
        self.current_round_number += 1

    def deal(self, source_pile: Stack, dest_piles: list[Stack], card_cnt: int, dealer_idx: int | None = None) -> None:
        dealer_idx = dealer_idx if dealer_idx is not None else self.dealer_idx
        ordered_dest_piles = dest_piles[dealer_idx + 1 % len(dest_piles):] + dest_piles[:dealer_idx + 1]
        [p.push(source_pile.pop()) for _ in range(card_cnt) for p in ordered_dest_piles]
