from collections import defaultdict, Counter
from dataclasses import dataclass, field, InitVar
import random

from gamenacki.common.card_pile import CardPile
from gamenacki.forbiddenislandnacki.models.adventurers import ADVENTURERS, Adventurer, Explorer, Messenger
from gamenacki.forbiddenislandnacki.models.board import Board
from gamenacki.forbiddenislandnacki.models.piles import Piles
from gamenacki.forbiddenislandnacki.models.tiles import Tile, TileHeight
from gamenacki.forbiddenislandnacki.models.treasures import Treasure, TREASURES
from gamenacki.forbiddenislandnacki.models.treasure_cards import TreasureCard, TreasureCardWatersRise
from gamenacki.forbiddenislandnacki.models.waters import WaterMeter, WATER_LEVELS


ADVENTURER_STARTING_TILES = {'Diver': 'Iron Gate', 'Engineer': 'Bronze Gate', 'Explorer': 'Copper Gate',
                             'Messenger': 'Silver Gate', 'Navigator': 'Gold Gate', 'Pilot': "Fools' Landing"}


@dataclass
class PlayerMove:
    ...


@dataclass
class GameState:
    player_cnt: int
    initial_water_level_int: int = 0
    board: Board = field(default_factory=Board)
    water_meter: WaterMeter = field(init=False)
    piles: Piles = field(default_factory=Piles)
    treasures_collected: list[Treasure] = field(default_factory=list)
    hands: tuple[CardPile, ...] = field(init=False)
    adventurers: tuple[Adventurer] = field(init=False)
    adventurer_coords: dict[str: tuple[int, int]] = field(default_factory=dict)
    player_turn_idx: int = field(init=False)

    def __post_init__(self):
        self.water_meter = WaterMeter(WATER_LEVELS[self.initial_water_level_int])

        # the island starts to sink; 6 random tiles are flooded
        for flood_card in random.sample(self.piles.flood_cards.cards, 6):
            t = next(t for t in self.board.tiles if t.name == flood_card.name)
            t.sink()

        self.hands = tuple(CardPile() for _ in range(self.player_cnt))

        self.adventurers = tuple(random.sample(ADVENTURERS, self.player_cnt))

        for a in self.adventurers:
            tile_row_idx, tile_col_idx = self.board.get_tile_coord_by_name(ADVENTURER_STARTING_TILES[a.name])
            self.adventurer_coords[a.name] = (tile_row_idx, tile_col_idx)

        # deal cards to players; Waters Rise! cards are shuffled back into deck and re-tried
        for _ in range(12):
            for h in self.hands:
                while isinstance(self.piles.treasure_cards.cards[-1], TreasureCardWatersRise):
                    random.shuffle(self.piles.treasure_cards.cards)
                h.push(self.piles.treasure_cards.cards.pop())

        self.player_turn_idx = random.choice([_ for _ in range(self.player_cnt)])

    def deal(self) -> None:
        pass

    @property
    def is_game_over(self) -> bool:
        # TODO: all of the other conditions
        return self.water_meter.is_death_level

    @property
    def coord_adventurers(self) -> dict[tuple[int, int]: list[str]]:
        d = defaultdict(list)
        for adv_str, coords in self.adventurer_coords.items():
            d[coords].append(adv_str)
        return d

    def get_possible_shores(self, player_idx: int) -> tuple[tuple[int, int, Tile], ...]:
        """example return: ((2, 2, Gold Gate), (2, 3, Howling Garden), ...)"""
        adv_coord = self.adventurer_coords[self.adventurers[player_idx].name]
        adj_tiles = self.board.get_adjacent_tiles(adv_coord)
        diag_tiles = self.board.get_adjacent_tiles(adv_coord)
        same_tile = self.board.get_same_tile(adv_coord)
        if isinstance(self.adventurers[player_idx], Explorer):
            possible_tiles = [same_tile] + adj_tiles + diag_tiles
        else:
            possible_tiles = [same_tile] + adj_tiles
        return tuple([t for t in possible_tiles if t[2].height == TileHeight.FLOODED])

    def get_possible_movements(self, player_idx: int) -> tuple[tuple[int, int, Tile], ...]:
        """example return: ((2, 2, Gold Gate), (2, 3, Howling Garden), ...)"""
        adv_coord = self.adventurer_coords[self.adventurers[player_idx].name]
        adj_tiles = self.board.get_adjacent_tiles(adv_coord)
        diag_tiles = self.board.get_adjacent_tiles(adv_coord)
        possible_tiles = adj_tiles + diag_tiles if isinstance(self.adventurers[player_idx], Explorer) else adj_tiles
        return tuple([t for t in possible_tiles])

    def get_possible_treasure_passes(self, player_idx: int) -> list[tuple[int, TreasureCard, int, str]]:
        """example return: [(0, 'Sandbags', 1, 'Pilot'), ...] =
        giving your hand's 0 index card Sandbags to player idx 1 the Pilot.
        this class GameState does not have knowledge of 'Player' so the player names aren't known"""
        my_coord = self.adventurer_coords[self.adventurers[player_idx].name]
        my_hand = [(idx, card) for idx, card in enumerate(self.hands[player_idx])]
        same_tile_adventurers = [(idx, adv_role) for idx, (adv_role, adv_coord) in enumerate(self.adventurer_coords.items())
                                 if adv_coord == my_coord and idx != player_idx]
        all_other_adventurers = [(i, adv.name) for i, adv in enumerate(self.adventurers) if i != player_idx]
        eligible_recipients = same_tile_adventurers if not isinstance(self.adventurers[player_idx], Messenger) else same_tile_adventurers + all_other_adventurers
        return [(c_idx, c, player_i, adv_name) for c_idx, c in my_hand for (player_i, adv_name) in eligible_recipients]

    def get_possible_collect_treasure(self, player_idx: int) -> Treasure | None:
        """example return: The Earth Stone"""
        treasure_card_ctr_most_popular = Counter([c.name for c in self.hands[player_idx]]).most_common(1)
        if treasure_card_ctr_most_popular[0][1] >= 4:
            treasure_name = treasure_card_ctr_most_popular[0][0]
            return next((t for t in TREASURES if t == treasure_name and t not in self.treasures_collected), None)
        return None

    def move_adventurer(self, player_idx: int, new_row: int, new_col: int) -> None:
        self.adventurer_coords[self.adventurers[player_idx].name] = (new_row, new_col)

    def shore_tile(self, tile_row: int, tile_col: int) -> None:
        self.board.spaces[tile_row][tile_col].shore()

    def pass_treasure_card(self, player_idx: int, card_idx: int, recipient_player_idx: int) -> None:
        self.hands[recipient_player_idx].append(self.hands[player_idx].pop(card_idx))

    def collect_treasure(self, player_idx: int) -> None:
        collectable_treasure = self.get_possible_collect_treasure(player_idx)
        if not collectable_treasure:
            return
        source_hand = self.hands[player_idx]
        redeemed_cards = []
        for card in source_hand.cards[:]:
            if card.name == collectable_treasure.value and len(redeemed_cards) < 4:
                redeemed_cards.append(card)
                source_hand.remove(card)
        self.piles.treasure_card_discard.cards.extend(redeemed_cards)
        self.treasures_collected.append(collectable_treasure)

    def do_turn(self):
        ...
