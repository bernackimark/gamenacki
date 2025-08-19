from dataclasses import dataclass, field

from gamenacki.common.base_engine import BaseEngine
from gamenacki.common.log import Event, Log
from gamenacki.forbiddenislandnacki.models.constants import Action
from gamenacki.forbiddenislandnacki.models.game_state import GameState, PlayerMove
from gamenacki.forbiddenislandnacki.players import Player, ConsolePlayer
from gamenacki.forbiddenislandnacki.renderers import Renderer, ConsoleRenderer

@dataclass
class Engine(BaseEngine):
    players: list[Player]
    renderer: Renderer
    gs: GameState = None
    log: Log = field(default_factory=Log)

    def __post_init__(self):
        if not self.gs:
            self.gs = GameState(self.player_cnt)
        for idx, p in enumerate(self.players):
            p.adventurer = self.gs.adventurers[idx]
        self.log.push(Event(self.gs, Action.BEGIN_GAME))

    @property
    def player_cnt(self) -> int:
        return len(self.players)

    def play(self) -> None:
        while not self.gs.is_game_over:
            self.log.push(Event(self.gs, Action.BEGIN_TURN))
            turn_idx = self.gs.player_turn_idx
            player = self.players[turn_idx]

            self.renderer.render(self.gs, self.players)

            player_move: PlayerMove = player.make_move(self.gs)



e = Engine(players=[ConsolePlayer(0, 'Mark', False), ConsolePlayer(1, 'Valerie', False)],
           renderer=ConsoleRenderer())
e.play()


#
#     try:
#         player_move: PlayerMove = player.make_move(self.gs.piles.hands[turn_idx], self.gs)
#         move: Move = self.gs.make_move(turn_idx, player_move)
#         self.log.push(Event(move.after_state, move.action, move.player_idx))
#     except Exception as ex:
#         self.renderer.render_error(ex)
#
#     if self.gs.is_round_over:
#         self.gs.assign_points()
#         self.renderer.render(self.gs, self.players)
#         self.log.push(Event(self.gs, Action.END_TURN))
#         time.sleep(2)
#         self.gs.create_new_round()
#
# self.renderer.render(self.gs, self.players)
# self.log.push(Event(self.gs, Action.END_GAME))
# self.renderer.render_log(self.log)
