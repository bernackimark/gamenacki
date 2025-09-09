from abc import abstractmethod
from dataclasses import dataclass

from gamenacki.common.base_player import BasePlayer
from gamenacki.forbiddenislandnacki.models.adventurers import Adventurer
from gamenacki.forbiddenislandnacki.models.game_state import GameState


@dataclass
class Player(BasePlayer):
    adventurer: Adventurer = None

    @property
    def name_and_role(self) -> str:
        return f'{self.name} the {self.adventurer.name}'

    @staticmethod
    @abstractmethod
    def make_move(gs: GameState) -> "PlayerMove":
        ...


@dataclass
class ConsolePlayer(Player):
    def make_move(self, gs: GameState) -> "PlayerMove":
        possible_actions = gs.possible_actions
        for i, p in enumerate(possible_actions):
            print(i, p)
        move_idx = int(input("Please make your move selection: "))
        return possible_actions[move_idx]

