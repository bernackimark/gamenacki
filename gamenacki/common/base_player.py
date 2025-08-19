from abc import ABC
from dataclasses import dataclass

@dataclass
class BasePlayer(ABC):
    idx: int
    name: str
    is_bot: bool  # isn't defaulted as subclasses would be forced into default values downstream

