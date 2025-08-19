from abc import abstractmethod
from dataclasses import dataclass, field
import random

from gamenacki.common.base_player import BasePlayer
from gamenacki.forbiddenislandnacki.models.adventurers import Adventurer
from gamenacki.forbiddenislandnacki.models.game_state import GameState, PlayerMove
# from gamenacki.lostcitinacki.models.cards import Card
# from gamenacki.lostcitinacki.models.constants import DrawFromStack, PlayToStack
# from gamenacki.lostcitinacki.models.game_state import GameState, PlayerMove
# from gamenacki.lostcitinacki.models.piles import Hand


@dataclass
class Player(BasePlayer):
    adventurer: Adventurer = None

    @property
    def name_and_role(self) -> str:
        return f'{self.name} the {self.adventurer.name}'

    @staticmethod
    @abstractmethod
    def make_move(gs: GameState) -> PlayerMove:
        ...


@dataclass
class ConsolePlayer(Player):
    def make_move(self, gs: GameState) -> PlayerMove:
        possible_movements = gs.get_possible_movements(self.idx)
        print('Possible Movements: ', [_ for _ in possible_movements])
        possible_shores = gs.get_possible_shores(self.idx)
        print('Possible Shores: ', [_ for _ in possible_shores])
        possible_treasure_cards_passes = gs.get_possible_treasure_passes(self.idx)
        print('Possible Treasure Card Passes: ', [_ for _ in possible_treasure_cards_passes])
        possible_treasure_collect = gs.get_possible_collect_treasure(self.idx)
        print('Possible Treasure Collection: ', possible_treasure_collect)
        the_input: str = input("Please select your action: Move, Shore, Pass, Collect (ex: 'm24', 's02', 'p11', 'c') ")

        if the_input[0] == 'm':
            gs.move_adventurer(self.idx, int(the_input[1]), int(the_input[2]))
        elif the_input[0] == 's':
            gs.shore_tile(int(the_input[1]), int(the_input[2]))
        elif the_input[0] == 'p':
            gs.pass_treasure_card(self.idx, int(the_input[1]), int(the_input[2]))
        elif the_input[0] == 'c':
            gs.collect_treasure(self.idx)


    # @staticmethod
    # def make_move(h: Hand, gs: GameState) -> PlayerMove:
    #     options = h.get_possible_moves(gs.board_playable_cards, len(gs.piles.discard.cards) > 0)
    #     possible_player_moves: list[PlayerMove] = [PlayerMove(c, pts, dfs) for c, pts, dfs in options]
    #     while True:
    #         try:
    #             sel_card, exp_or_discard, deck_or_discard = input('card, e/d, de/di (R7 e de) ').strip().split()
    #             card: Card | None = next((c for c in h if c.__repr__() == sel_card), None)
    #             play_to_stack = PlayToStack.EXPEDITION if exp_or_discard == 'e' else PlayToStack.DISCARD
    #             draw_from_stack = DrawFromStack.DECK if deck_or_discard == 'de' else DrawFromStack.DISCARD
    #             move = PlayerMove(card, play_to_stack, draw_from_stack)
    #             if move in possible_player_moves:
    #                 return move
    #         except Exception as e:
    #             raise e
    #             # TODO: do i have access to Renderer.render_error() from here?
    #             #  or should i not try/except here, but rather in the engine?
