from enum import StrEnum


class Treasure(StrEnum):
    EARTH_STONE = 'The Earth Stone'
    STATUE_OF_THE_WIND = 'The Statue of the Wind'
    CRYSTAL_OF_FIRE = 'The Crystal of Fire'
    OCEAN_CHALICE = "The Ocean's Chalice"

    def __repr__(self) -> str:
        return str(self.value)


TREASURES = [_ for _ in Treasure]
