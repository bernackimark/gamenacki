from enum import StrEnum, auto


class Action:
    BEGIN_GAME = auto()
    BEGIN_TURN = auto()
    PLAYER_MOVE = auto()
    END_TURN = auto()
    END_GAME = auto()


class Color(StrEnum):
    BLACK = auto()
    RED = auto()
    GREEN = auto()
    GRAY = auto()
    YELLOW = auto()
    BLUE = auto()


ANSI_COLOR_CODES = {
    Color.BLACK: "\033[30m",
    Color.RED: "\033[31m",
    Color.GREEN: "\033[32m",
    Color.GRAY: "\033[90m",  # also called "bright black"
    Color.YELLOW: "\033[33m",
    Color.BLUE: "\033[34m"}
ANSI_COLOR_RESET = "\033[0m"
