# base_constants.py
"""Contains enums"""

from enum import StrEnum, auto

from gamenacki.common.base_constants import BaseAction

class Action(BaseAction):
    BEGIN_GAME = auto()
    BEGIN_ROUND = auto()
    PLAYER_MOVE = auto()
    END_ROUND = auto()
    END_GAME = auto()


class Color(StrEnum):
    YELLOW = auto()
    BLUE = auto()
    WHITE = auto()
    GREEN = auto()
    RED = auto()


class PlayToStack(StrEnum):
    EXPEDITION = auto()
    DISCARD = auto()


class DrawFromStack(StrEnum):
    DECK = auto()
    DISCARD = auto()
