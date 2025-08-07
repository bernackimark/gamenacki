from dataclasses import dataclass, field

from cardnacki.constants import VIDEO_POKER_HANDS
from cardnacki.describe_poker_hand import describe_poker_hand
from cardnacki.pile import Card, create_cards_from_rank_suits, Deck
from gamenacki.common.base_game_state import BaseGameState
from gamenacki.common.dealer import Dealer
from gamenacki.common.scorer import Scorer, Ledger
from gamenacki.common.stack import Stack
from gamenacki.videopokernacki.models.constants import PRIZE_TABLE
from gamenacki.videopokernacki.models.piles import Piles


# @dataclass(frozen=True)
# class Move:
#     action: Action
#     player_idx: int
#     before_state: "GameState"
#     after_state: "GameState"


@dataclass
class GameState(BaseGameState):
    """parent attributes are:
        player_cnt: int
        piles: Piles
        scorer: Scorer
        dealer: Dealer
    """

    def __post_init__(self):
        self.scorer.ledgers[0].add_a_value(100)

    max_draws: int = 1
    draw_cnt: int = 0
    wager: int = 0
    prize_table: dict[str: int] = field(default_factory=lambda: PRIZE_TABLE.copy())
    possible_hands: tuple[str] = VIDEO_POKER_HANDS

    @classmethod
    def create_game_state(cls, player_cnt: int, max_draws: int):
        return cls(player_cnt=player_cnt, piles=Piles(),
                   scorer=Scorer([Ledger()]),
                   dealer=Dealer(player_cnt), max_draws=max_draws)

    @property
    def has_game_started(self) -> bool:
        pass

    @property
    def is_game_over(self) -> bool:
        return self.is_round_over and self.scorer.ledgers[0].total == 0

    @property
    def is_round_over(self) -> bool:
        return self.draw_cnt == self.max_draws

    @property
    def hand_description(self) -> str:
        return describe_poker_hand(self.piles.hand.cards, self.possible_hands)

    def get_hand_description(self, cards: list[Card]):
        return describe_poker_hand(cards, self.possible_hands)

    def create_piles(self) -> list[Stack]:
        """Not needed because all piles are being created in piles.py"""

    def decrement_balance(self, bet: int) -> None:
        if bet > self.scorer.ledgers[0].total:
            raise ValueError("You don't have enough funds")
        self.scorer.ledgers[0].add_a_value(bet * -1)

    def increment_balance(self, amt: int) -> None:
        self.scorer.ledgers[0].add_a_value(amt)

    def calculate_prize(self, outcome_str: str, wager: int = 1) -> int:
        return self.prize_table.get(outcome_str, 0) * (self.wager or wager)

    def create_new_round(self):
        self.piles.hand.clear()
        self.piles.deck = Deck(True)
        self.draw_cnt = 0
        self.dealer.increment_round_number()

    def deal(self, card_cnt: int = 5, explicit_cards: list[Card] | str = None) -> None:
        if explicit_cards:
            cards = create_cards_from_rank_suits(self.piles.deck, explicit_cards) if isinstance(explicit_cards, str) else explicit_cards
            for c in cards:
                self.piles.hand.append(c)
                self.piles.deck.remove(c)
        else:
            for _ in range(card_cnt):
                self.piles.hand.push(self.piles.deck.cards.pop())

    def draw(self, held_cards: list[Card]) -> None:
        for idx, card in enumerate(self.piles.hand.cards):
            if card not in held_cards:
                self.piles.hand.remove(card)
                self.piles.hand.cards.insert(idx, self.piles.deck.cards.pop())
        self.draw_cnt += 1
