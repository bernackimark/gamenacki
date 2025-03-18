from dataclasses import dataclass

from gamenacki.lostcitinacki.models.constants import Color


@dataclass
class Card:
    color: Color
    value: int


@dataclass
class Handshake(Card):
    value: int = 0

    def __repr__(self) -> str:
        return f'{self.color[0].upper()}H'


@dataclass
class ExpeditionCard(Card):
    def __repr__(self) -> str:
        return f'{self.color[0].upper()}{self.value}'
