import random
from dataclasses import dataclass, InitVar, field
from enum import Enum

from gamenacki.forbiddenislandnacki.models.adventurers import Adventurer, Color

from gamenacki.forbiddenislandnacki.models.tiles import Tile, TILES, TileHeight

BOARD_STANDARD = ((0, 0, 1, 1, 0, 0),
                  (0, 1, 1, 1, 1, 0),
                  (1, 1, 1, 1, 1, 1),
                  (1, 1, 1, 1, 1, 1),
                  (0, 1, 1, 1, 1, 0),
                  (0, 0, 1, 1, 0, 0))


@dataclass
class Empty:
    def __repr__(self) -> str:
        return f'{"":^18}'


@dataclass
class Board:
    @dataclass
    class TileDirection(Enum):
        SAME = [(0, 0)]
        ADJACENT = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        DIAGONAL = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # up-left, up-right, down-left, down-right
        DOUBLE_ADJACENT = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1), (0, -2), (-2, 0), (0, 2), (2, 0)]
        ALL_OTHER = [(r, c) for r in range(-5, 6) for c in range(-5, 6) if (r, c) != (0, 0)]  # warning: hard-coded

    all_tiles: InitVar[tuple[Tile, ...]] = TILES
    tile_arrangement: InitVar[tuple[tuple[int, ...], ...]] = BOARD_STANDARD
    spaces: tuple[tuple[Tile | Empty, ...], ...] = None

    def __post_init__(self, all_tiles: tuple[Tile], tile_arrangement: tuple[tuple[int, ...]]):
        tiles = list(all_tiles)
        random.shuffle(tiles)
        self.spaces = tuple(tuple(tiles.pop() if bit else Empty() for bit in row) for row in tile_arrangement)
        for r_i, row in enumerate(self.spaces):
            for c_i, tile in enumerate(row):
                if isinstance(tile, Tile):
                    tile.x = r_i
                    tile.y = c_i

    def __repr__(self) -> str:
        return "\n".join(" ".join([str(s) for s in row]) for row in self.spaces)

    @property
    def tiles(self) -> tuple[Tile, ...]:
        return tuple(space for row in self.spaces for space in row if isinstance(space, Tile))

    def get_tile_by_coord(self, row: int, col: int) -> Tile:
        return next(t for t in self.tiles if t.x == row and t.y == col)

    def get_tile_coord_by_name(self, tile_name: str) -> tuple[int, int]:
        for r_idx, row in enumerate(self.spaces):
            for c_idx, space in enumerate(row):
                if isinstance(space, Tile) and space.name == tile_name:
                    return r_idx, c_idx
        raise ValueError(f"I couldn't find a tile named {tile_name}")

    def get_tiles(self, coord: tuple[int, int], directions: TileDirection) -> list[Tile]:
        row_cnt, col_cnt = len(self.spaces), len(self.spaces[0])
        neighbors = []
        for dr, dc in directions.value:
            r, c = coord[0] + dr, coord[1] + dc
            if 0 <= r < row_cnt and 0 <= c < col_cnt and isinstance(self.spaces[r][c], Tile):
                neighbors.append(self.spaces[r][c])
        return neighbors

    def get_all_other_tiles(self, coord: tuple[int, int]) -> list[Tile]:
        return [t for t in self.tiles if (t.x, t.y) != coord]
