import time
from dataclasses import dataclass, field

from gamenacki.common.base_engine import BaseEngine
from gamenacki.common.base_renderer import Renderer
from gamenacki.common.log import Log, Event
from gamenacki.lostcitinacki.models.constants import Action
from gamenacki.lostcitinacki.models.game_state import GameState, Move, PlayerMove
from gamenacki.lostcitinacki.players import Player


@dataclass
class LostCities(BaseEngine):
    players: list[Player]
    renderer: Renderer
    gs: GameState = None
    log: Log = field(default_factory=Log)
    max_rounds: int = 3

    def __post_init__(self):
        if not self.gs:
            self.gs = GameState.create_game_state(self.player_cnt, self.max_rounds)
        self.log.push(Event(self.gs, Action.BEGIN_GAME))

    @property
    def player_cnt(self) -> int:
        return len(self.players)

    def play(self) -> None:
        while not self.gs.is_game_over:
            self.log.push(Event(self.gs, Action.BEGIN_ROUND))
            self.renderer.render(self.gs, self.players)
            turn_idx = self.gs.dealer.player_turn_idx
            player = self.players[turn_idx]
            try:
                player_move: PlayerMove = player.make_move(self.gs.piles.hands[turn_idx], self.gs)
                move: Move = self.gs.make_move(turn_idx, player_move)
                self.log.push(Event(move.after_state, move.action, move.player_idx))
            except Exception as ex:
                self.renderer.render_error(ex)

            if self.gs.is_round_over:
                self.gs.assign_points()
                self.renderer.render(self.gs, self.players)
                self.log.push(Event(self.gs, Action.END_ROUND))
                time.sleep(2)
                self.gs.create_new_round()

        self.renderer.render(self.gs, self.players)
        self.log.push(Event(self.gs, Action.END_GAME))
        self.renderer.render_log(self.log)
