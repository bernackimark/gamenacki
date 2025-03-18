import time

from gamenacki.common.log import Log
from gamenacki.common.base_renderer import Renderer
from gamenacki.lostcitinacki.players import Player
from gamenacki.lostcitinacki.models.game_state import GameState


class ConsoleRenderer(Renderer):
    def render(self, gs: GameState, players: list[Player]) -> None:
        if not gs.has_round_started:
            print(f"This is round #{gs.dealer.current_round_number} of {gs.max_rounds}")
            print(f"{players[gs.dealer.dealer_idx].name} is the dealer; {players[gs.dealer.player_turn_idx].name} plays first")
            print()

        if not gs.is_game_over:
            print('Their Expeditions:', gs.piles.exp_boards[1].expeditions)
            print('Discard:', gs.piles.discard.cards[-1] if gs.piles.discard.cards else '[]', 'Deck:',
                  '*' * len(gs.piles.deck.cards))
            print('Your Expeditions: ', gs.piles.exp_boards[0].expeditions)
            print('Your Hand:', gs.piles.hands[0].cards)
            print()

        if gs.is_round_over:
            print('Round is over')
            for p, ledger in zip(players, gs.scorer.ledgers):
                print(f'{p.name} has {ledger.total} {"points" if ledger.total != 1 else "point"}')
            print()

        if gs.is_game_over:
            print('Game is over')
            if isinstance(gs.winner, tuple):
                winner_idx, points = gs.winner
                print(f"The winner is {players[winner_idx].name} with "
                      f"{points} {'point' if points == 1 else 'points'}")
            else:
                winner_names = 'and '.join([p.name for i, p in enumerate(players) for idx in gs.winner if i == idx])
                points = gs.winner[0][1]
                print(f"{winner_names} tied with {points} {'points' if gs.scorer.ledgers[0].total != 1 else 'point'}")
            print('Thank you for playing.  Goodbye!\n')
            time.sleep(2)

    def render_error(self, exc: Exception) -> None:
        print(f"Something's gone wrong: {exc}")
        print()

    def render_log(self, game_log: Log) -> None:
        for event in game_log:
            print(event)
