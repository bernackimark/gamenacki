import random
from dataclasses import dataclass, InitVar, field

from gamenacki.forbiddenislandnacki.models.adventurers import Adventurer, Color

from gamenacki.forbiddenislandnacki.models.tiles import Tile, TILES, TileHeight

BOARD_STANDARD = ((0, 0, 1, 1, 0, 0),
                  (0, 1, 1, 1, 1, 0),
                  (1, 1, 1, 1, 1, 1),
                  (1, 1, 1, 1, 1, 1),
                  (0, 1, 1, 1, 1, 0),
                  (0, 0, 1, 1, 0, 0))

# TODO: The Messenger & Navigator sharing a tile is dorking the tile's repr

@dataclass
class Empty:
    def __repr__(self) -> str:
        return f'{"":^18}'


@dataclass
class Board:
    all_tiles: InitVar[tuple[Tile, ...]] = TILES
    tile_arrangement: InitVar[tuple[tuple[int, ...], ...]] = BOARD_STANDARD
    spaces: tuple[tuple[Tile | Empty, ...], ...] = None

    def __post_init__(self, all_tiles: tuple[Tile], tile_arrangement: tuple[tuple[int, ...]]):
        tiles = list(all_tiles)
        random.shuffle(tiles)
        self.spaces = tuple(tuple(tiles.pop() if bit else Empty() for bit in row) for row in tile_arrangement)

        # self.spaces = tuple(tuple(tiles.pop() if bit else Empty() for bit in row) for row in tile_arrangement)

        # spaces = [[None if bit else Empty() for bit in row] for row in tile_arrangement]
        # for r_idx, row in enumerate(spaces):
        #     for c_idx, space in enumerate(row):
        #         if space is None:
        #             tile = tiles.pop()
        #             spaces[r_idx][c_idx] = tile
        #             tile.board_coord = r_idx, c_idx
        # self.spaces = tuple(tuple(_ for _ in row) for row in spaces)

    def __repr__(self) -> str:
        return "\n".join(" ".join([str(s) for s in row]) for row in self.spaces)

    @property
    def tiles(self) -> tuple[Tile, ...]:
        return tuple(space for row in self.spaces for space in row if isinstance(space, Tile))

    def get_tile_coord_by_name(self, tile_name: str) -> tuple[int, int]:
        for r_idx, row in enumerate(self.spaces):
            for c_idx, space in enumerate(row):
                if isinstance(space, Tile) and space.name == tile_name:
                    return r_idx, c_idx
        raise ValueError(f"I couldn't find a tile named {tile_name}")

    def get_adjacent_tiles(self, coord: tuple[int, int]) -> list[tuple[int, int, Tile]] | list[None]:
        row_cnt, col_cnt = len(self.spaces), len(self.spaces[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        neighbors = []
        for dr, dc in directions:
            r, c = coord[0] + dr, coord[1] + dc
            if 0 <= r < row_cnt and 0 <= c < col_cnt and isinstance(self.spaces[r][c], Tile):
                neighbors.append((r, c, self.spaces[r][c]))
        return neighbors

    def get_diagonal_tiles(self, coord: tuple[int, int]) -> list[tuple[int, int, Tile]] | list[None]:
        row_cnt, col_cnt = len(self.spaces), len(self.spaces[0])
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # up-left, up-right, down-left, down-right

        neighbors = []
        for dr, dc in directions:
            r, c = coord[0] + dr, coord[1] + dc
            if 0 <= r < row_cnt and 0 <= c < col_cnt and isinstance(self.spaces[r][c], Tile):
                neighbors.append((r, c, self.spaces[r][c]))
        return neighbors

    def get_same_tile(self, coord: tuple[int, int]) -> tuple[int, int, Tile]:
        return coord[0], coord[1], self.spaces[coord[0]][coord[1]]
