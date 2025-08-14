from dataclasses import dataclass, field, InitVar
from enum import auto, StrEnum
import random

class Treasure(StrEnum):
    EARTH_STONE = 'The Earth Stone'
    STATUE_OF_THE_WIND = 'The Statue of the Wind'
    CRYSTAL_OF_FIRE = 'The Crystal of Fire'
    OCEAN_CHALICE = "The Ocean's Chalice"

    def __repr__(self) -> str:
        return self.value


TREASURES = [_ for _ in Treasure]


class AdventurerType(StrEnum):
    DIVER = 'Diver'
    ENGINEER = 'Engineer'
    EXPLORER = 'Explorer'
    MESSENGER = 'Messenger'
    NAVIGATOR = 'Navigator'
    PILOT = 'Pilot'


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

@dataclass
class Adventurer:
    role: AdventurerType
    color: Color
    special_power_text: str


ADVENTURERS = (
    Adventurer(AdventurerType.DIVER, Color.BLACK, 'does dive stuff'),
    Adventurer(AdventurerType.ENGINEER, Color.RED, 'shores up 2'),
    Adventurer(AdventurerType.EXPLORER, Color.GREEN, 'move/shore diagonally'),
    Adventurer(AdventurerType.MESSENGER, Color.GRAY, 'pass treasures anywhere'),
    Adventurer(AdventurerType.NAVIGATOR, Color.YELLOW, 'move another player <=2 adjacent spaces for 1 action'),
    Adventurer(AdventurerType.PILOT, Color.BLUE, 'once per turn, fly to any tile')
)


class TileHeight(StrEnum):
    NORMAL = auto()
    FLOODED = auto()
    SUNKEN = auto()

@dataclass
class Tile:
    name: str
    img: str = ''
    treasure: Treasure = None
    height: TileHeight = TileHeight.NORMAL
    starting_tile_for: AdventurerType = None
    is_exit: bool = False
    adventurers: list[Adventurer] = field(default_factory=list)

    def __repr__(self) -> str:
        # TODO: place into Console Renderer
        if not self.adventurers:
            return f'{self.repr_():^18}'
        if len(self.adventurers) == 1:
            return f'{ANSI_COLOR_CODES.get(self.adventurers[0].color)}{self.repr_():^18}{ANSI_COLOR_RESET}'
        if len(self.adventurers) > 1:
            # TODO: the :^18 isn't working as expected
            char_chunk_size = len(self.name) // len(self.adventurers)
            char_chunks = [self.repr_()[i:i + char_chunk_size] for i in range(0, len(self.name), char_chunk_size)]
            ansi_chars = []
            for idx, char_chunk in enumerate(char_chunks):
                text = f'{ANSI_COLOR_CODES.get(self.adventurers[idx].color)}{char_chunk}'
                ansi_chars.append(text)
            final_ansi_str = ''.join([_ for _ in ansi_chars])
            return f'{final_ansi_str:^18}{ANSI_COLOR_RESET}'

    def repr_(self) -> str:
        if self.height == TileHeight.NORMAL:
            return self.name.upper()
        if self.height == TileHeight.FLOODED:
            return self.name.lower()
        return ' ' * 18


TILES = (
    Tile('Watchtower'), Tile('Breakers Bridge'), Tile('Dunes of Deception'), Tile('Phantom Rock'),
    Tile('Twilight Hollow'), Tile('Crimson Forest'), Tile('Cliffs of Abandon'), Tile('Lost Lagoon'),
    Tile('Misty Marsh'), Tile('Observatory'),
    Tile('Gold Gate', starting_tile_for=AdventurerType.NAVIGATOR),
    Tile('Bronze Gate', starting_tile_for=AdventurerType.ENGINEER),
    Tile('Silver Gate', starting_tile_for=AdventurerType.MESSENGER),
    Tile('Iron Gate', starting_tile_for=AdventurerType.DIVER),
    Tile('Copper Gate', starting_tile_for=AdventurerType.EXPLORER),
    Tile("Fools' Landing", starting_tile_for=AdventurerType.PILOT, is_exit=True),
    Tile('Cave of Embers', treasure=Treasure.CRYSTAL_OF_FIRE),
    Tile('Cave of Shadows', treasure=Treasure.CRYSTAL_OF_FIRE),
    Tile('Temple of the Moon', treasure=Treasure.EARTH_STONE),
    Tile('Temple of the Sun', treasure=Treasure.EARTH_STONE),
    Tile('Howling Garden', treasure=Treasure.STATUE_OF_THE_WIND),
    Tile('Whispering Garden', treasure=Treasure.STATUE_OF_THE_WIND),
    Tile('Coral Palace', treasure=Treasure.OCEAN_CHALICE),
    Tile('Tidal Palace', treasure=Treasure.OCEAN_CHALICE)
)


@dataclass
class TreasureCard:
    name: str
    is_action: bool
    action_text: str = None


def create_treasure_cards() -> list[TreasureCard]:
    treasures: list[TreasureCard] = [TreasureCard(t, False) for t in Treasure for _ in range(5)]
    waters_rise: list[TreasureCard] = [TreasureCard('Waters Rise!', True, 'do the waters rise thing') for _ in range(3)]
    helicopter_lift: list[TreasureCard] = [TreasureCard('Helicopter Lift', True, 'use at any time, fly some people') for _ in range(3)]
    sandbags: list[TreasureCard] = [TreasureCard('Sandbags', True, 'shore up any tile') for _ in range(2)]
    return treasures + waters_rise + helicopter_lift + sandbags


@dataclass
class TreasureCardPile:
    cards: list[TreasureCard] = field(default_factory=create_treasure_cards)

    def __post_init__(self):
        random.shuffle(self.cards)

@dataclass
class TreasureDiscardPile:
    cards: list[TreasureCard] = field(default_factory=list)


@dataclass
class FloodCard:
    name: str
    img: str = ''

    def __repr__(self) -> str:
        return self.name

@dataclass
class FloodCardPile:
    cards: list[FloodCard] = field(default_factory=lambda: [FloodCard(t.name, t.img) for t in TILES])

    def __post_init__(self):
        random.shuffle(self.cards)

@dataclass
class FloodDiscardPile:
    cards: list[FloodCard] = field(default_factory=list)

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
            level_repr_list.append(str(level_repr))
        return ' '.join(level_repr_list)

    def waters_rise(self) -> WaterLevel:
        current_level_idx = WATER_LEVELS.index(self.current_level)
        self.current_level = WATER_LEVELS[current_level_idx + 1]
        return self.current_level

    @property
    def is_death_level(self) -> bool:
        return self.current_level.is_death


BOARD_STANDARD = ((0, 0, 1, 1, 0, 0),
                  (0, 1, 1, 1, 1, 0),
                  (1, 1, 1, 1, 1, 1),
                  (1, 1, 1, 1, 1, 1),
                  (0, 1, 1, 1, 1, 0),
                  (0, 0, 1, 1, 0, 0))


@dataclass
class Empty:
    def __repr__(self) -> str:
        return f'{"":^18}'


@dataclass
class Board:
    all_tiles: InitVar[tuple[Tile, ...]]
    tile_arrangement: InitVar[tuple[tuple[int, ...], ...]]
    spaces: tuple[tuple[Tile | Empty, ...], ...] = None

    def __post_init__(self, all_tiles: tuple[Tile], tile_arrangement: tuple[tuple[int, ...]]):
        tiles = list(all_tiles)
        random.shuffle(tiles)
        self.spaces = tuple(tuple(tiles.pop() if bit else Empty() for bit in row) for row in tile_arrangement)

    @property
    def tiles(self) -> list[Tile]:
        """Scans 'self.spaces', skips all non-tiles, returns a single list of Tiles"""
        return [s for row in self.spaces for s in row if isinstance(s, Tile)]

    def print_board(self) -> None:
        for row in self.spaces:
            print([_ for _ in row])

    def place_adventurers_at_starting_tiles(self, adventurers: tuple[Adventurer, ...]) -> None:
        for a in adventurers:
            for t in self.tiles:
                if t.starting_tile_for == a.role:
                    t.adventurers.append(a)


@dataclass
class GameState:
    player_cnt: int
    board: Board
    water_meter: WaterMeter
    piles: list = field(init=False)

    def __post_init__(self):
        self.create_piles()

    def create_piles(self) -> None:
        ...
        # TODO: move piles to piles.py.  create a Piles dataclass that pulls them all together
        #   have all of the piles inherit from Stack.

    @property
    def is_game_over(self) -> bool:
        # TODO: all of the other conditions
        return self.water_meter.is_death_level

    def do_turn(self):
        ...


# setup game
b = Board(TILES, BOARD_STANDARD)
water_meter = WaterMeter(WATER_LEVELS[0])
treasure_card_pile = TreasureCardPile()
treasure_discard_pile = TreasureDiscardPile()
flood_card_pile = FloodCardPile()
flood_discard_pile = FloodDiscardPile()
treasures_collected: list[Treasure] = []

# the island starts to sink; 6 random tiles are flooded
for flood_card in random.sample(flood_card_pile.cards, 6):
    for t in b.tiles:
        if flood_card.name == t.name:
            t.is_flooded = True

player_cnt = 2
player_names = ['Alice', 'Bob']
hands: list[list[TreasureCard]] = [[] for _ in range(player_cnt)]

adventurers = random.sample(ADVENTURERS, player_cnt)
b.place_adventurers_at_starting_tiles(adventurers)
b.print_board()

# deal cards to players; Waters Rise! cards are shuffled back into deck and re-tried
for _ in range(2):
    for h in hands:
        while True:
            card = treasure_card_pile.cards[-1]
            if card.name == 'Waters Rise!':
                random.shuffle(treasure_card_pile.cards)
            else:
                h.append(treasure_card_pile.cards.pop())
                break
for h in hands:
    print([c.name for c in h])

turn_idx = random.choice([_ for _ in range(player_cnt)])
print(f"{player_names[turn_idx]} will go first!")


gs = GameState(player_cnt, b, water_meter)

