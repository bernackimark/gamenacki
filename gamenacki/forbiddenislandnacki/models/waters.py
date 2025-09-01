from dataclasses import dataclass, field

from gamenacki.forbiddenislandnacki.models.constants import ANSI_COLOR_CODES, ANSI_COLOR_RESET, Color


@dataclass
class WaterLevel:
    draw_cnt: int
    starting_name: str = None
    is_death: bool = False


WATER_LEVELS = (WaterLevel(2, 'Novice'), WaterLevel(2, 'Normal'), WaterLevel(3, 'Elite'), WaterLevel(3, 'Legendary'),
                WaterLevel(3), WaterLevel(4), WaterLevel(4), WaterLevel(5), WaterLevel(5), WaterLevel(0, 'Death', True))

@dataclass
class WaterMeter:
    starting_level: WaterLevel
    current_level: WaterLevel = field(init=False)
    water_levels: tuple = WATER_LEVELS

    def __post_init__(self):
        self.current_level = self.starting_level

    def __repr__(self) -> str:
        level_repr_list = []
        for level in self.water_levels:
            if level == self.current_level:
                level_repr = f'{ANSI_COLOR_CODES.get(Color.BLUE)}{level.draw_cnt}{ANSI_COLOR_RESET}'
            else:
                level_repr = level.draw_cnt
            level_repr_list.append(str(level_repr) if not level.is_death else '☠')
        return ' '.join(level_repr_list)

    def waters_rise(self) -> WaterLevel:
        current_level_idx = WATER_LEVELS.index(self.current_level)
        self.current_level = WATER_LEVELS[current_level_idx + 1]
        return self.current_level

    @property
    def is_death_level(self) -> bool:
        return self.current_level.is_death



