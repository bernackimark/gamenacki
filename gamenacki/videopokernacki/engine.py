import time
from dataclasses import dataclass, field
from enum import Enum, auto
from itertools import combinations

from cardnacki.card import Card
from cardnacki.describe_poker_hand import describe_poker_hand_from_lu_job
from cardnacki.pile import create_cards_from_rank_suits, Deck
from gamenacki.common.base_engine import BaseEngine
from gamenacki.common.base_renderer import Renderer
from gamenacki.common.log import Log, Event
from gamenacki.videopokernacki.models.constants import Action, NO_DRAW_LIKELIHOOD
from gamenacki.videopokernacki.models.game_state import GameState
from gamenacki.videopokernacki.players import Player


class DisplayOrReturnData(Enum):
    DISPLAY = auto()
    RETURN = auto()


@dataclass
class VideoPoker(BaseEngine):
    players: list[Player]
    renderer: Renderer
    gs: GameState = None
    log: Log = field(default_factory=Log)
    max_draws: int = 1

    def __post_init__(self):
        if not self.gs:
            self.gs = GameState.create_game_state(self.player_cnt, self.max_draws)
        self.log.push(Event(self.gs, Action.BEGIN_GAME))

    @property
    def player_cnt(self) -> int:
        return len(self.players)

    def play(self) -> None:
        while not self.gs.is_game_over:
            player = self.players[0]  # player count is hard-coded at 1
            # try:
            if not len(self.gs.piles.hand.cards):
                self.log.push(Event(self.gs, Action.BEGIN_ROUND))
                self.renderer.render(self.gs, self.players)
                self.gs.wager = player.get_wager(self.gs.scorer.ledgers[0].total)
                self.gs.decrement_balance(self.gs.wager)
                self.gs.deal(5)
                self.renderer.render(self.gs, self.players)
            elif self.gs.draw_cnt < self.max_draws:
                held_cards: list[Card] = player.get_held_cards(self.gs)
                self.gs.draw(held_cards)
                self.renderer.render(self.gs, self.players)
                time.sleep(2)
                self.log.push(Event(self.gs, Action.DRAW))
            # except Exception as ex:
            #     self.renderer.render_error(ex)

            elif self.gs.is_round_over:
                prize = self.gs.calculate_prize(self.gs.hand_description)
                self.gs.increment_balance(prize)
                self.renderer.render(self.gs, self.players)
                self.log.push(Event(self.gs, Action.END_ROUND))
                time.sleep(2)
                self.gs.create_new_round()

            else:
                raise ValueError("I shouldn't reach here")

        self.log.push(Event(self.gs, Action.END_GAME))
        self.renderer.render_log(self.log)

    @staticmethod
    def draw_all_combos(held_cards: list[Card], d: Deck) -> list[list[Card]]:
        """From given held cards, return held cards and all possibilities of drawn cards"""
        return [held_cards + list(combo) for combo in combinations(d.cards, 5 - len(held_cards))]

    def get_outcome_stats(self, hands: list[list[Card]]) -> dict[str: tuple[float, float]]:
        """For all hands, return {'Royal Flush': [.0005, 1.3] ...} .0005 is the frequency, 1.3 is the avg prize"""
        total_hand_cnt = len(hands)
        outcome_dict = {outcome: [0, 0] for outcome in self.gs.possible_hands}
        for h in hands:
            hand_desc: str = self.gs.get_hand_description(h)
            outcome_dict[hand_desc][0] += 1
            outcome_dict[hand_desc][1] += self.gs.calculate_prize(hand_desc)
        return {outcome: (cnt / total_hand_cnt, prize_sum / total_hand_cnt)
                for outcome, (cnt, prize_sum) in outcome_dict.items()}

    def play_held_card_outcomes(self, display_or_return_data: DisplayOrReturnData) -> dict[str: tuple[float, float]] | None:
        """User selects between 0 and 5 cards; for that selection, run all 5 card possibilities to obtain the
        relative likelihood & average prize amount by outcome.  Either render it or return it to the caller."""
        held_cards_str: str = self.players[0].select_sim_cards()
        held_cards: list[Card] = create_cards_from_rank_suits(self.gs.piles.deck, held_cards_str)

        if not len(held_cards):  # if user wants 5 random cards, use the pre-saved data to save processing power
            self.renderer.render_outcome_possibilities(NO_DRAW_LIKELIHOOD)
            return
        elif len(held_cards) > 5:
            self.renderer.render_error(ValueError("You must select between 0 and 5 cards"))
            return

        all_hands = self.draw_all_combos(held_cards, self.gs.piles.deck)
        outcome_stats = self.get_outcome_stats(all_hands)

        if display_or_return_data == DisplayOrReturnData.DISPLAY:
            self.renderer.render_outcome_possibilities(outcome_stats)
        else:
            return outcome_stats

    def get_all_outcomes(self, cards: list[Card]) -> list[tuple[list[Card], float]]:
        """For a hand of cards, returns held cards & average prize.  Ex:
        [([Ts 🂠, Js 🂠, Qs 🂠, Ks 🂠, As 🂠], 976.0), ([Ts 🂠, Js 🂠, Qs 🂠, Ks 🂠], 21.63) ... ([], 0.34)]"""
        results = []
        all_held_card_combos: list[list[Card]] = [list(combo) for r in range(6) for combo in combinations(cards, r)]  # 32 combinations
        for held_cards in all_held_card_combos:
            all_combos = self.draw_all_combos(held_cards, self.gs.piles.deck)  # between 0 and 2M+ combinations
            avg_prize = sum([self.gs.calculate_prize(self.gs.get_hand_description(hand)) for hand in all_combos]) / len(all_combos)
            results.append((held_cards, avg_prize))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get_all_outcomes_from_lookup(self, cards: list[Card]) -> list[tuple[list[Card], float]]:
        results = []
        all_held_card_combos: list[list[Card]] = [list(combo) for r in range(6) for combo in combinations(cards, r)]
        for held_cards in all_held_card_combos:
            all_combos = self.draw_all_combos(held_cards, self.gs.piles.deck)  # between 0 and 2M+ combinations
            avg_prize = sum([self.gs.calculate_prize(describe_poker_hand_from_lu_job(hand)) for hand in all_combos]) / len(all_combos)
            results.append((held_cards, avg_prize))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

