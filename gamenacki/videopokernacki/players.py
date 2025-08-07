from abc import abstractmethod
from dataclasses import dataclass

from gamenacki.common.base_player import BasePlayer
from gamenacki.videopokernacki.models.cards import Card
from gamenacki.videopokernacki.models.game_state import GameState


@dataclass
class Player(BasePlayer):
    @staticmethod
    @abstractmethod
    def get_wager(bal: int) -> int:
        ...

    @abstractmethod
    def get_held_cards(self, gs: GameState) -> list[Card]:
        ...


@dataclass
class ConsolePlayer(Player):
    @staticmethod
    def get_wager(bal: int) -> int:
        while True:
            wager = int(input(f"Your balance is ${bal}. How much do you want to wager? "))
            if not 0 < wager <= bal:
                print("Invalid wager")
            else:
                return wager

    def get_held_cards(self, gs: GameState) -> list[Card] | list[None]:
        hold_indices_str: str = input('Select which card indices to hold (ex. 135) ')
        if not hold_indices_str:
            return []
        held_indices = [int(x) - 1 for x in hold_indices_str]
        return [c for idx, c in enumerate(gs.piles.hand.cards) if idx in held_indices]

    @staticmethod
    def select_sim_cards() -> str:
        return input("Select cards to hold and then run sim ('As Ks Qs Js Ts'): ")
