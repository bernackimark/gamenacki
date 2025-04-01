from abc import ABC, abstractmethod
from dataclasses import dataclass
import random

from gamenacki.common.base_player import BasePlayer
from gamenacki.lostcitinacki.models.cards import Card
from gamenacki.lostcitinacki.models.constants import DrawFromStack, PlayToStack
from gamenacki.lostcitinacki.models.game_state import GameState, PlayerMove
from gamenacki.lostcitinacki.models.piles import Hand


@dataclass
class Player(BasePlayer):
    @staticmethod
    @abstractmethod
    def make_move(h: Hand, gs: GameState) -> PlayerMove:
        ...


@dataclass
class ConsolePlayer(Player):
    @staticmethod
    def make_move(h: Hand, gs: GameState) -> PlayerMove:
        options = h.get_possible_moves(gs.board_playable_cards, len(gs.piles.discard.cards) > 0)
        possible_player_moves: list[PlayerMove] = [PlayerMove(c, pts, dfs) for c, pts, dfs in options]
        while True:
            try:
                sel_card, exp_or_discard, deck_or_discard = input('card, e/d, de/di (R7 e de) ').strip().split()
                card: Card | None = next((c for c in h if c.__repr__() == sel_card), None)
                play_to_stack = PlayToStack.EXPEDITION if exp_or_discard == 'e' else PlayToStack.DISCARD
                draw_from_stack = DrawFromStack.DECK if deck_or_discard == 'de' else DrawFromStack.DISCARD
                move = PlayerMove(card, play_to_stack, draw_from_stack)
                if move in possible_player_moves:
                    return move
            except Exception as e:
                raise e
                # TODO: do i have access to Renderer.render_error() from here?
                #  or should i not try/except here, but rather in the engine?


@dataclass
class RandomBot(Player):
    @staticmethod
    def make_move(h: Hand, gs: GameState) -> PlayerMove:
        """Chooses a valid move at random"""
        options: list[tuple[Card, PlayToStack, DrawFromStack]] = h.get_possible_moves(gs.board_playable_cards, len(gs.piles.discard.cards) > 0)
        possible_player_moves: list[PlayerMove] = [PlayerMove(c, pts, dfs) for c, pts, dfs in options]
        return random.choice(possible_player_moves)

@dataclass
class BullBot(Player):
    @staticmethod
    def make_move(h: Hand, gs: GameState) -> tuple[Card, PlayToStack, DrawFromStack]:
        ...
        # TODO: make this bot rules-based

@dataclass
class ColleenBot(Player):
    @staticmethod
    def make_move(h: Hand, gs: GameState) -> tuple[Card, PlayToStack, DrawFromStack]:
        ...
        # TODO: monte carlo sims
