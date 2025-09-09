from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
import random

from gamenacki.common.card_pile import CardPile
from gamenacki.forbiddenislandnacki.models.actions import AdvMove, AdvShore, AdvPassCard, AdvCollectTreasure, \
    AdvPlaySandbags, AdvPlayHeliLift, AdvDiscard, AdvEndTurn
from gamenacki.forbiddenislandnacki.models.adventurers import ADVENTURERS, Adventurer, Explorer, Messenger, Navigator, Pilot
from gamenacki.forbiddenislandnacki.models.board import Board
from gamenacki.forbiddenislandnacki.models.constants import Action
from gamenacki.forbiddenislandnacki.models.piles import Piles
from gamenacki.forbiddenislandnacki.models.tiles import Tile, TileHeight
from gamenacki.forbiddenislandnacki.models.treasures import Treasure
from gamenacki.forbiddenislandnacki.models.treasure_cards import (TreasureCardWatersRise,
                                                                  TreasureCardSandbags, TreasureCardHelicopterLift,
                                                                  TreasureCardTreasure)
from gamenacki.forbiddenislandnacki.models.waters import WaterMeter, WATER_LEVELS

MAX_ACTIONS_PER_TURN = 3
MAX_CARDS_IN_HAND = 5


@dataclass(frozen=True)
class Move:
    action: Action
    player_idx: int
    before_state: "GameState"
    after_state: "GameState"


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
    turn_pilot_flights: int = field(init=False, default=0)
    turn_action_cnt: int = field(init=False, default=0)
    is_player_willingly_passing_the_turn: bool = field(init=False, default=False)

    def __post_init__(self):
        self.water_meter = WaterMeter(WATER_LEVELS[self.initial_water_level_int])

        # the island starts to sink; 6 random tiles are flooded
        for flood_card in random.sample(self.piles.flood_cards.cards, 6):
            t = next(t for t in self.board.tiles if t.name == flood_card.name)
            t.sink()

        self.hands = tuple(CardPile() for _ in range(self.player_cnt))

        self.adventurers = tuple(random.sample(ADVENTURERS, self.player_cnt))

        for a in self.adventurers:
            starting_tile: Tile = next(t for t in self.board.tiles if t.name == a.starting_tile_name)
            self.adventurer_coords[a.name] = starting_tile.x, starting_tile.y

        # deal cards to players; Waters Rise! cards are shuffled back into deck and re-tried
        for _ in range(2):
            for h in self.hands:
                while isinstance(self.piles.treasure_cards.peek(), TreasureCardWatersRise):
                    random.shuffle(self.piles.treasure_cards.cards)
                h.push(self.piles.treasure_cards.cards.pop())

        self.player_turn_idx = random.choice([_ for _ in range(self.player_cnt)])

    def deal_treasure_cards(self) -> None:
        drawn_card_cnt = 0
        while not drawn_card_cnt == 2:
            if not len(self.piles.treasure_cards):
                self.piles.treasure_cards.cards = self.piles.treasure_card_discard.cards
                self.piles.treasure_card_discard.clear()
                self.piles.treasure_cards.shuffle()
            while isinstance(self.piles.treasure_cards.peek(), TreasureCardWatersRise) and drawn_card_cnt == 1:
                print("Shuffling ...")
                self.piles.treasure_cards.shuffle()
            card = self.piles.treasure_cards.pop()
            if not isinstance(card, TreasureCardWatersRise):
                self.hands[self.player_turn_idx].push(card)
            else:
                self.water_meter.waters_rise()
                print("WATERS RISE!!!")
                # since both drawn cards are happening here, there's no ability to check for game over after 1st card
            drawn_card_cnt += 1

    def deal_flood_cards(self) -> None:
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

    @property
    def my_coord(self) -> tuple[int, int]:
        return self.adventurer_coords[self.my_role.name]
    
    @property
    def my_role(self) -> Adventurer:
        return self.adventurers[self.player_turn_idx]
    
    @property
    def my_hand(self) -> CardPile:
        return self.hands[self.player_turn_idx]

    @property
    def possible_shores(self) -> list[AdvShore]:
        """example return: (AdvShore(0, 2, 3, Gold Gate) =
        player 0 is shoring up the tile at coordinates (2, 3), which is Gold Gate"""
        same_tile = self.board.get_tiles(self.my_coord, self.board.TileDirection.SAME)

        if isinstance(self.my_role, Explorer):
            possible_tiles = (same_tile + self.board.get_tiles(self.my_coord, self.board.TileDirection.ADJACENT) +
                              self.board.get_tiles(self.my_coord, self.board.TileDirection.DIAGONAL))
        else:
            possible_tiles = same_tile + self.board.get_tiles(self.my_coord, self.board.TileDirection.ADJACENT)
        return [(AdvShore(self.player_turn_idx, t)) for t in possible_tiles if t.height == TileHeight.FLOODED]

    @property
    def possible_movements(self) -> list[AdvMove]:
        """example return: ((AdvMove(0, 2, 3, Gold Gate), ) =
        player 0 is moving to the tile at coordinates (2, 3), which is Gold Gate.
        Pilot can move to all other tiles, once per turn; Explorers can move diagonal as well as adjacent;
        Navigator can move self adjacent & all others double adjacent; All others can move adjacent"""

        if isinstance(self.my_role, Explorer):
            possible_tiles = (self.board.get_tiles(self.my_coord, self.board.TileDirection.ADJACENT) +
                              self.board.get_tiles(self.my_coord, self.board.TileDirection.DIAGONAL))
            return [AdvMove(self.player_turn_idx, t) for t in possible_tiles]
        if isinstance(self.my_role, Pilot) and self.turn_pilot_flights == 0:
            possible_tiles = self.board.get_tiles(self.my_coord, self.board.TileDirection.ALL_OTHER)
            return [AdvMove(self.player_turn_idx, t) for t in possible_tiles]
        if isinstance(self.my_role, Navigator):
            nav_possible_tiles = self.board.get_tiles(self.my_coord, self.board.TileDirection.ADJACENT)
            all_adv_moves = [AdvMove(self.player_turn_idx, t) for t in nav_possible_tiles]
            for i, other_adv in enumerate(self.adventurers):
                if i == self.player_turn_idx:
                    continue
                other_adv_coord = self.adventurer_coords[self.adventurers[i].name]
                other_adv_tiles = self.board.get_tiles(other_adv_coord, self.board.TileDirection.DOUBLE_ADJACENT)
                all_adv_moves.extend([AdvMove(i, t) for t in other_adv_tiles])
            return all_adv_moves

        possible_tiles = self.board.get_tiles(self.my_coord, self.board.TileDirection.ADJACENT)
        return [AdvMove(self.player_turn_idx, t) for t in possible_tiles]

    @property
    def possible_treasure_passes(self) -> list[AdvPassCard]:
        """example return: AdvPassCard((0, 4, 1, 'Pilot', 'The Earth Stone'), ...) =
        player 0 giving their 4th indexed card to player 1 the pilot; the card is The Earth Stone.
        this class GameState does not have knowledge of 'Player' so the player names aren't known.
        The Messenger can give a card to anyone; all others can only give cards to adventurers on their tile"""
        my_t_cards = [(i, card) for i, card in enumerate(self.my_hand) if isinstance(card, TreasureCardTreasure)]
        same_tile_adventurers = [(i, adv_role) for i, (adv_role, adv_coord) in enumerate(self.adventurer_coords.items())
                                 if adv_coord == self.my_coord and i != self.player_turn_idx]
        all_other_adventurers = [(i, adv.name) for i, adv in enumerate(self.adventurers) if i != self.player_turn_idx]
        eligible_recipients = same_tile_adventurers if not isinstance(self.my_role, Messenger) else same_tile_adventurers + all_other_adventurers
        return [AdvPassCard(self.player_turn_idx, c_idx, player_i, adv_name, c) for c_idx, c in my_t_cards for (player_i, adv_name) in eligible_recipients]

    @property
    def possible_collect_treasure(self) -> AdvCollectTreasure | None:
        """example return: AdvCollectTreasure(0, The Earth Stone) = player 0 collects The Earth Stone"""
        my_tile_treasure: Treasure = self.board.get_tile_by_coord(self.my_coord[0], self.my_coord[1]).treasure
        if not my_tile_treasure or my_tile_treasure in self.treasures_collected:
            return None
        if [c.name for c in self.my_hand.cards].count(my_tile_treasure.value) < 4:
            return None
        return AdvCollectTreasure(self.player_turn_idx, my_tile_treasure)

    @property
    def possible_sandbags(self) -> list[AdvPlaySandbags] | list[None]:
        flooded_tile_spaces = [t for t in self.board.tiles if t.height == TileHeight.FLOODED]
        adv_play_sandbags = []
        for h_i, h in enumerate(self.hands):
            for c_i, c in enumerate(h.cards):
                if isinstance(c, TreasureCardSandbags):
                    for t in flooded_tile_spaces:
                        adv_play_sandbags.append(AdvPlaySandbags(self.player_turn_idx, h_i, c_i, t))
        return adv_play_sandbags

    @property
    def possible_helicopter_lifts(self) -> list[AdvPlayHeliLift] | list[None]:
        adv_play_heli = []
        heli_cards = [(h_i, c_i) for h_i, h in enumerate(self.hands) for c_i, c in enumerate(h.cards)
                      if isinstance(c, TreasureCardHelicopterLift)]
        adv_coord_combos = {}
        for coord, roles in self.coord_adventurers.items():
            combos = [combo for r in range(1, len(roles) + 1) for combo in combinations(roles, r)]
            adv_coord_combos[coord] = combos
        for hand_idx, card_idx in heli_cards:
            for coord, role_combos in adv_coord_combos.items():
                source_tile: Tile = self.board.get_tile_by_coord(coord[0], coord[1])
                for dest_tile in self.board.get_all_other_tiles(coord):
                    for role_combo in role_combos:
                        adv_play_heli.append(AdvPlayHeliLift(self.player_turn_idx, hand_idx, card_idx, role_combo,
                                                             source_tile, dest_tile))
        return adv_play_heli

    @property
    def possible_discards(self) -> list[AdvDiscard] | None:
        """Player does not get the option to discard if they are not over the max"""
        if len(self.my_hand.cards) <= MAX_CARDS_IN_HAND:
            return None
        return [AdvDiscard(self.player_turn_idx, c_idx, c) for c_idx, c in enumerate(self.my_hand.cards)]

    @property
    def possible_actions(self) -> tuple[
        AdvMove | AdvShore | AdvPassCard | AdvCollectTreasure | AdvPlaySandbags | AdvPlayHeliLift | AdvEndTurn | AdvDiscard, ...]:
        if (discards := self.possible_discards) and (self.turn_action_cnt == MAX_ACTIONS_PER_TURN or self.is_player_willingly_passing_the_turn):
            return tuple(discards)

        if self.turn_action_cnt >= MAX_ACTIONS_PER_TURN or self.is_player_willingly_passing_the_turn:
            self.pass_the_turn()

        actions = [AdvEndTurn(self.player_turn_idx)] + self.possible_movements + self.possible_shores + \
                  self.possible_treasure_passes + [self.possible_collect_treasure] + self.possible_sandbags + \
                  self.possible_helicopter_lifts

        return tuple([a for a in actions if a])

    def move_adventurer(self, player_idx: int, new_row: int, new_col: int) -> None:
        self.adventurer_coords[self.adventurers[player_idx].name] = (new_row, new_col)

    def shore_tile(self, tile_row: int, tile_col: int) -> None:
        self.board.spaces[tile_row][tile_col].shore()

    def pass_treasure_card(self, card_idx: int, recipient_player_idx: int) -> None:
        self.hands[recipient_player_idx].push(self.my_hand.pop(card_idx))

    def collect_treasure(self) -> None:
        collectable_treasure = self.possible_collect_treasure.treasure
        if not collectable_treasure:
            return
        redeemed_cards = []
        for card in self.my_hand.cards[:]:
            if card.name == collectable_treasure.value and len(redeemed_cards) < 4:
                redeemed_cards.append(card)
                self.my_hand.remove(card)
        self.piles.treasure_card_discard.cards.extend(redeemed_cards)
        self.treasures_collected.append(collectable_treasure)

    def play_sandbags(self, aps: AdvPlaySandbags):
        self.shore_tile(aps.tile.x, aps.tile.y)
        self.piles.treasure_card_discard.push(self.hands[aps.card_owner_idx].cards.pop(aps.card_in_hand_idx))

    def play_heli_lift(self, aph: AdvPlayHeliLift):
        for adv_role in aph.player_roles_to_move:
            self.adventurer_coords[adv_role] = (aph.dest_tile.x, aph.dest_tile.y)
        self.piles.treasure_card_discard.push(self.hands[aph.card_owner_idx].cards.pop(aph.card_in_hand_idx))

    def play_discard(self, ad: AdvDiscard):
        self.piles.treasure_card_discard.push(self.hands[ad.player_id].cards.pop(ad.card_in_hand_idx))

    def pass_the_turn(self):
        if self.possible_discards:
            return

        self.deal_treasure_cards()
        if self.is_game_over:
            return

        self.deal_flood_cards()
        if self.is_game_over:
            return

        self.turn_pilot_flights = 0
        self.turn_action_cnt = 0
        self.is_player_willingly_passing_the_turn = False
        self.player_turn_idx = (self.player_turn_idx + 1) % self.player_cnt

    def was_pilot_action_a_flight(self, new_row: int, new_col: int) -> bool:
        current_row, current_col = self.adventurer_coords['Pilot']
        row_cnt = new_row - current_row
        col_cnt = new_col - current_col
        if (row_cnt, col_cnt) not in self.board.TileDirection.ADJACENT.value:
            return True
        return False

    def make_move(self, action: AdvMove | AdvShore | AdvPassCard | AdvCollectTreasure | AdvPlaySandbags | AdvPlayHeliLift | AdvEndTurn | AdvDiscard):
        if isinstance(action, AdvDiscard):
            self.play_discard(action)
            return
        if isinstance(action, AdvEndTurn):
            self.is_player_willingly_passing_the_turn = True
            self.pass_the_turn()
            return
        if isinstance(action, AdvMove):
            if isinstance(self.adventurers[self.player_turn_idx], Pilot):
                if self.was_pilot_action_a_flight(action.tile.x, action.tile.y):
                    self.turn_pilot_flights += 1
            self.move_adventurer(action.player_id, action.tile.x, action.tile.y)
        elif isinstance(action, AdvShore):
            self.shore_tile(action.tile.x, action.tile.y)
        elif isinstance(action, AdvPassCard):
            self.pass_treasure_card(action.from_player_card_idx, action.to_player_id)
        elif isinstance(action, AdvCollectTreasure):
            self.collect_treasure()
        elif isinstance(action, AdvPlaySandbags):
            self.play_sandbags(action)
        elif isinstance(action, AdvPlayHeliLift):
            self.play_heli_lift(action)
        else:
            raise ValueError("Unknown action")

        if not isinstance(action, (AdvPlaySandbags, AdvPlayHeliLift)):
            self.turn_action_cnt += 1
        if self.turn_action_cnt == MAX_ACTIONS_PER_TURN:
            self.pass_the_turn()

    # TODO:
    #  movement:
    #    The Diver may move through one or more adjacent missing and/or flooded tiles for 1 action.
    #  shore:
    #    Engineer is only charged a w one action to shore up two w/o moving
    #  passing the turn; players having too many cards; it's a mess and needs review !!!
    #  drawing treasure cards doesn't yield a card back one at a time, so no ability to see waters rise
    #  drawing cards & flipping flood tiles should await user input and only allow those things to happen?
    #  flip flood tiles equal to the WaterLevel
    #  when tile is sunken, all adventurers on the tile must select an adjacent tile (or they may die)

