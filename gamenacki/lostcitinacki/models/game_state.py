from copy import deepcopy
from dataclasses import dataclass

from gamenacki.common.base_game_state import BaseGameState
from gamenacki.common.dealer import Dealer
from gamenacki.common.piles import Discard
from gamenacki.common.scorer import Ledger, WinCondition, Scorer
from gamenacki.lostcitinacki.models.cards import Card
from gamenacki.lostcitinacki.models.constants import Action, Color, PlayToStack, DrawFromStack
from gamenacki.lostcitinacki.models.piles import ExpeditionBoard, Deck, Hand, Piles

@dataclass(frozen=True)
class Move:
    action: Action
    player_idx: int
    before_state: "GameState"
    after_state: "GameState"

@dataclass
class PlayerMove:
    card: Card
    play_to_stack: PlayToStack
    draw_from_stack: DrawFromStack

@dataclass
class GameState(BaseGameState):
    """parent attributes are:
        player_cnt: int
        piles: Piles
        scorer: Scorer
        dealer: Dealer
    """
    max_rounds: int

    def __post_init__(self):
        self.create_piles()
        self.deal()

    @classmethod
    def create_game_state(cls, player_cnt: int, max_rounds: int):
        return cls(player_cnt=player_cnt, piles=Piles(),
                   scorer=Scorer([Ledger() for _ in range(player_cnt)], WinCondition.HIGHEST_SCORE_W_TIES),
                   dealer=Dealer(player_cnt), max_rounds=max_rounds)

    @property
    def has_game_started(self) -> bool:
        return self.has_round_started or self.dealer.current_round_number > 1

    @property
    def is_game_over(self) -> bool:
        return self.is_round_over and self.dealer.current_round_number >= self.max_rounds

    @property
    def has_round_started(self) -> bool:
        return self.piles.discard.cards or any([exp.cards for exp_board in self.piles.exp_boards for exp in exp_board])

    @property
    def is_round_over(self) -> bool:
        return len(self.piles.deck.cards) == 0 or set(self.color_maxes.values()) == {10}

    @property
    def winner(self) -> None | tuple[int, int] | list[tuple[int, int]]:
        """Returns None if game not over; tuple[player_idx, points] if solo winner else list[tuple[]] for ties"""
        if not self.is_game_over:
            return None
        return self.scorer.get_winner(self.is_game_over)

    @property
    def color_maxes(self) -> dict[Color: int]:
        return {c: max([p.get_max_card_in_color(c) for p in self.piles.exp_boards]) for c in list(Color)}

    @property
    def board_playable_cards(self) -> list[Card]:
        fresh_deck = Deck()
        return [c for c in fresh_deck if c.value > self.color_maxes[c.color] or self.color_maxes[c.color] == 0]

    @property
    def is_discard_card_playable(self) -> bool:
        return self.piles.discard.peek() in self.board_playable_cards

    def create_piles(self) -> None:
        for _ in range(self.player_cnt):
            self.piles.hands.append(Hand())
            self.piles.exp_boards.append(ExpeditionBoard())

    def create_new_round(self):
        [h.clear() for h in self.piles.hands]
        [e.clear() for e in self.piles.exp_boards]
        self.piles.deck = Deck()
        self.piles.discard = Discard()
        self.dealer.advance_button()
        self.dealer.set_player_idx_as_left_of_dealer()
        self.deal()
        self.dealer.increment_round_number()

    def deal(self, card_cnt: int = 8):
        self.dealer.deal(self.piles.deck, [_ for _ in self.piles.hands], card_cnt)

    def make_move(self, player_idx: int, move: PlayerMove) -> Move:
        before_state = deepcopy(self)
        hand = self.piles.hands[player_idx]
        exp_board = self.piles.exp_boards[player_idx]
        try:
            hand.remove(move.card)
            if move.play_to_stack == PlayToStack.DISCARD:
                self.piles.discard.push(move.card)
                hand.push(self.piles.deck.pop())
            if move.play_to_stack == PlayToStack.EXPEDITION:
                dest_pile = next(pile for pile in exp_board.expeditions if pile.color == move.card.color)
                dest_pile.push(move.card)
                hand.push(self.piles.deck.pop() if move.draw_from_stack == DrawFromStack.DECK else self.piles.discard.pop())
            self.dealer.advance_turn()
            return Move(Action.PLAYER_MOVE, player_idx, before_state, self)
        except Exception as e:
            raise e

    def assign_points(self) -> None:
        for pl, exp_board in zip(self.scorer.ledgers, self.piles.exp_boards):
            pl.add_a_value(exp_board.points)
