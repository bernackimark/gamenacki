
# from gamenacki.common.log import Log
from gamenacki.common.base_renderer import Renderer
from gamenacki.forbiddenislandnacki.players import Player
from gamenacki.forbiddenislandnacki.models.adventurers import ADVENTURER_NAME_COLORS
from gamenacki.forbiddenislandnacki.models.board import Tile, Empty, TileHeight
from gamenacki.forbiddenislandnacki.models.game_state import GameState
from gamenacki.forbiddenislandnacki.models.constants import ANSI_COLOR_CODES, ANSI_COLOR_RESET


class ConsoleRenderer(Renderer):
    def render(self, gs: GameState, players: list[Player]) -> None:
        self._clear()
        self._print_board(gs)
        print(f"Water Level {gs.water_meter} ... Treasures Collected: {[_ for _ in gs.treasures_collected]}")
        for idx, h in enumerate(gs.hands):
            print(f"{players[idx].name_and_role}'s hand: {sorted(h, key=lambda x: x.name)}")
        print(f"It's {players[gs.player_turn_idx].name_and_role}'s turn")

    def render_error(self, exc: Exception) -> None:
        pass

    def render_log(self, log) -> None:
        pass

    def _print_board(self, gs: GameState):
        board_ansi_colors = {coord: [ADVENTURER_NAME_COLORS[name] for name in adv_names] for coord, adv_names in
                             gs.coord_adventurers.items()}

        def _space_repr(space: Tile | Empty, r_idx: int, c_idx: int):
            """If the Tile has no adventurers, it prints to the console with standard white text.
            If one adventurer, it prints the color of the adventurer.
            If multiple adventurers, it prints a rainbow of the adventurer colors"""
            space_ansi_colors = board_ansi_colors.get((r_idx, c_idx))

            if not space_ansi_colors:
                return space.__repr__()

            ansi_colors = [ADVENTURER_NAME_COLORS[adv_name] for adv_name in gs.coord_adventurers[(r_idx, c_idx)]]

            if len(ansi_colors) == 1:
                return f'{ansi_colors[0]}{space.__repr__()}{ANSI_COLOR_RESET}'

            char_chunk_size = (len(space.__repr__()) // len(ansi_colors))
            char_chunks = [space.__repr__()[i:i + char_chunk_size] for i in range(0, len(space.__repr__()), char_chunk_size)]
            ansi_chars = []
            for idx, char_chunk in enumerate(char_chunks):
                text = f'{ansi_colors[idx]}{char_chunk}'
                ansi_chars.append(text)
            final_ansi_str = ''.join([_ for _ in ansi_chars])
            return f'{final_ansi_str:^18}{ANSI_COLOR_RESET}'

        space_reprs = []
        for r_idx, row in enumerate(gs.board.spaces):
            space_reprs.append([])
            for c_idx, space in enumerate(row):
                space_reprs[r_idx].append(f'{_space_repr(space, r_idx, c_idx):^18}')

        for row in space_reprs:
            print(" ".join(row))

    @staticmethod
    def _clear() -> None:
        print("\033[2J\033[H", end="")

