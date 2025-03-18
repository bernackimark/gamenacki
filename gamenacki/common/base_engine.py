"""ABC engine that expects attributes: Player(s), Renderer, Log, and GameState.
Its play method is what is run to play to the game.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from gamenacki.common.log import Log
from gamenacki.common.base_renderer import Renderer


@dataclass
class BaseEngine(ABC):
    players: list["Player"]
    renderer: Renderer
    gs: "GameState"
    log: Log

    @property
    def player_cnt(self) -> int:
        return len(self.players)

    @abstractmethod
    def play(self) -> None:
        """Example usage:
        def play(self) -> None:
            game_state = self.create_new_game()
            while True:
                while True:
                    self.renderer.render(game_state, self.players)
                    if game_state.is_round_over:
                        break
                    player = self.get_current_player(game_state)
                    try:
                        game_state = player.make_move(game_state)
                    except ValueError as ex:
                        if self.error_handler:
                            self.error_handler(ex)
                if game_state.is_game_over:
                    break
                game_state = self.create_new_round(game_state)
        """
        ...