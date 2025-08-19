from dataclasses import dataclass


@dataclass
class FloodCard:
    name: str
    img: str = ''

    def __repr__(self) -> str:
        return self.name
