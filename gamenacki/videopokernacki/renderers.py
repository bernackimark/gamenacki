import time

from gamenacki.common.log import Log
from gamenacki.common.base_renderer import Renderer
from gamenacki.videopokernacki.models.game_state import GameState
from gamenacki.videopokernacki.players import Player


class ConsoleRenderer(Renderer):
    def render(self, gs: GameState, players: list[Player]) -> None:
        print()
        print(f"Balance: ${gs.scorer.ledgers[0].total}. Your hand: {gs.piles.hand.cards}")
        if gs.draw_cnt == gs.max_draws:
            print(f'Outcome: {gs.hand_description}. Prize: {gs.calculate_prize(gs.hand_description)}')
        print()

    @staticmethod
    def render_outcome_possibilities(outcome_stats: dict[str: tuple[float, float]]) -> None:
        print(outcome_stats)

    def render_error(self, exc: Exception) -> None:
        print(f"Something's gone wrong: {exc}")
        print()

    def render_log(self, game_log: Log) -> None:
        for event in game_log:
            print(event)
