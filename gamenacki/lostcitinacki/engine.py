import time
from dataclasses import dataclass, field

from gamenacki.common.base_renderer import Renderer
from gamenacki.common.log import Log, Event
from gamenacki.common.piles import Discard

from gamenacki.lostcitinacki.models.constants import Color, DrawFromStack, Action
from gamenacki.lostcitinacki.models.game_state import GameState
from gamenacki.lostcitinacki.players import Player


@dataclass
class LostCities:
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
                selected_card, play_to_stack = player.play_card(self.gs.piles.hands[turn_idx], self.gs.board_playable_cards)
                color_or_discard: Color | Discard = self.gs.play_card_to(turn_idx, selected_card, play_to_stack)
                self.log.push(Event(self.gs, Action.PLAY_CARD, turn_idx))
                can_pick_up_discard: bool = not isinstance(color_or_discard, Discard) and len(self.gs.piles.discard) > 0
                drawing_from: DrawFromStack = player.pick_up_from(can_pick_up_discard, self.gs.is_discard_card_playable)
                self.gs.draw_from(turn_idx, drawing_from)
                self.log.push(Event(self.gs, Action.PICKUP_CARD, turn_idx))

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
