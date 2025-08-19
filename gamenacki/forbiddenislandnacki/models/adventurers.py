from abc import ABC
from dataclasses import dataclass

from gamenacki.forbiddenislandnacki.models.constants import Color, ANSI_COLOR_CODES


@dataclass
class Adventurer(ABC):
    color: Color
    special_power_text: str
    moves_and_shores: tuple[tuple[int, int]] = ((-1, 0), (1, 0), (0, -1), (0, 1))  # up, down, left, right
    shore_cnt_per_action: int = 1

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def ansi_color(self) -> str:
        return ANSI_COLOR_CODES.get(self.color)

@dataclass
class Diver(Adventurer):
    color: Color = Color.BLACK
    special_power_text: str = 'does dive stuff'

@dataclass
class Engineer(Adventurer):
    color: Color = Color.RED
    special_power_text: str = "The Engineer may shore up 2 tiles for 1 action"
    shore_cnt_per_action: int = 2

@dataclass
class Explorer(Adventurer):
    color: Color = Color.GREEN
    special_power_text: str = 'move/shore diagonally'
    moves_and_shores: tuple[tuple[int, int]] = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1))

@dataclass
class Messenger(Adventurer):
    color: Color = Color.GRAY
    special_power_text: str = 'pass treasures anywhere'

@dataclass
class Navigator(Adventurer):
    color: Color = Color.YELLOW
    special_power_text: str = 'move another player <=2 adjacent spaces for 1 action'

@dataclass
class Pilot(Adventurer):
    color: Color = Color.BLUE
    special_power_text: str = 'once per turn, fly to any tile'


ADVENTURERS = (Diver(), Engineer(), Explorer(), Messenger(), Navigator(), Pilot())

ADVENTURER_NAME_COLORS = {a.name: a.ansi_color for a in ADVENTURERS}
