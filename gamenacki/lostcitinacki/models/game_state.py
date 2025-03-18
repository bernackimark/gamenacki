from dataclasses import dataclass

from gamenacki.common.base_game_state import BaseGameState
from gamenacki.common.dealer import Dealer
from gamenacki.common.piles import Hand, Discard
from gamenacki.common.scorer import Ledger, WinCondition, Scorer
from gamenacki.lostcitinacki.models.cards import Card
from gamenacki.lostcitinacki.models.constants import Color, PlayToStack, DrawFromStack
from gamenacki.lostcitinacki.models.piles import ExpeditionBoard, Deck, Piles


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

    def play_card_to(self, p_idx: int, c: Card, dest_pile: PlayToStack) -> Color | Discard:
        hand = self.piles.hands[p_idx]
        exp_board = self.piles.exp_boards[p_idx]
        if c not in hand.cards:
            raise ValueError(f"{c} is not in the hand")
        if dest_pile == PlayToStack.DISCARD:
            return self._play_to_discard(hand, c)
        else:
            return self._play_to_exp_pile(hand, c, exp_board)

    def draw_from(self, p_idx: int, source_pile: DrawFromStack):
        hand = self.piles.hands[p_idx]
        returned_card = self.piles.deck.pop() if source_pile == DrawFromStack.DECK else self.piles.discard.pop()
        if not returned_card:
            raise ValueError("There are no cards here")
        hand.push(returned_card)
        self.dealer.player_turn_idx = self.dealer.next_player_idx()

    def _play_to_discard(self, h: Hand, c: Card) -> Discard:
        h.remove(c)
        self.piles.discard.push(c)
        return self.piles.discard

    def _play_to_exp_pile(self, h: Hand, c: Card, exp_board: ExpeditionBoard) -> Color:
        dest_pile = next(pile for pile in exp_board.expeditions if pile.color == c.color)
        max_number_in_color = max([p.get_max_card_in_color(c.color) for p in self.piles.exp_boards])
        if max_number_in_color > c.value > 0:
            raise ValueError(f"You must play higher than a {max_number_in_color}")
        h.remove(c)
        dest_pile.push(c)
        return dest_pile.color

    def assign_points(self) -> None:
        for pl, exp_board in zip(self.scorer.ledgers, self.piles.exp_boards):
            pl.add_a_value(exp_board.points)
