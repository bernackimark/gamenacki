from abc import ABC
from dataclasses import dataclass

@dataclass
class BasePlayer(ABC):
    idx: int
    name: str

