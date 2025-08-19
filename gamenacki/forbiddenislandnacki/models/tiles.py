from dataclasses import dataclass, field
from enum import StrEnum, auto

from gamenacki.forbiddenislandnacki.models.constants import ANSI_COLOR_CODES, ANSI_COLOR_RESET
from gamenacki.forbiddenislandnacki.models.treasures import Treasure


class TileHeight(StrEnum):
    NORMAL = auto()
    FLOODED = auto()
    SUNKEN = auto()


@dataclass
class Tile:
    name: str
    img: str = ''
    treasure: Treasure = None
    height: TileHeight = TileHeight.NORMAL
    is_exit: bool = False

    def __repr__(self) -> str:
        name = self.name.upper() if self.height == TileHeight.NORMAL else self.name.lower() if self.height == TileHeight.FLOODED else ' '
        return f'{name:^18}'

    def sink(self) -> None:
        if self.height == TileHeight.SUNKEN:
            return
        self.height = TileHeight.FLOODED if self.height == TileHeight.NORMAL else TileHeight.SUNKEN

    def shore(self) -> None:
        if self.height != TileHeight.FLOODED:
            return
        self.height = TileHeight.NORMAL


TILES = (
    Tile('Watchtower'), Tile('Breakers Bridge'), Tile('Dunes of Deception'), Tile('Phantom Rock'),
    Tile('Twilight Hollow'), Tile('Crimson Forest'), Tile('Cliffs of Abandon'), Tile('Lost Lagoon'),
    Tile('Misty Marsh'), Tile('Observatory'),
    Tile('Gold Gate'),
    Tile('Bronze Gate'),
    Tile('Silver Gate'),
    Tile('Iron Gate'),
    Tile('Copper Gate'),
    Tile("Fools' Landing", is_exit=True),
    Tile('Cave of Embers', treasure=Treasure.CRYSTAL_OF_FIRE),
    Tile('Cave of Shadows', treasure=Treasure.CRYSTAL_OF_FIRE),
    Tile('Temple of the Moon', treasure=Treasure.EARTH_STONE),
    Tile('Temple of the Sun', treasure=Treasure.EARTH_STONE),
    Tile('Howling Garden', treasure=Treasure.STATUE_OF_THE_WIND),
    Tile('Whispering Garden', treasure=Treasure.STATUE_OF_THE_WIND),
    Tile('Coral Palace', treasure=Treasure.OCEAN_CHALICE),
    Tile('Tidal Palace', treasure=Treasure.OCEAN_CHALICE)
)
