from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

from gamenacki.common.stack import Stack

if TYPE_CHECKING:
    from gamenacki.lostcitinacki.models.game_state import GameState
    from gamenacki.lostcitinacki.models.constants import Action

@dataclass(frozen=True)
class Event:
    game_state: "GameState"
    action: "Action"
    player_idx: int = None
    attributes: dict = field(default_factory=dict)
    timestamp: datetime = datetime.now()

    def __repr__(self) -> str:
        return (f"Timestamp: {self.timestamp}\n"
                f"Action: {self.action.name}\n"
                f"Player ID: {self.player_idx}\n"
                f"Game State: {self.game_state}\n"
                f"Attributes: {self.attributes}\n")


@dataclass
class Log(Stack):
    events: list[Event] = field(default_factory=list)
