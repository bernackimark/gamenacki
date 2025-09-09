from dataclasses import dataclass

from gamenacki.forbiddenislandnacki.models.tiles import Tile
from gamenacki.forbiddenislandnacki.models.treasure_cards import TreasureCard
from gamenacki.forbiddenislandnacki.models.treasures import Treasure


@dataclass(frozen=True)
class AdvMove:
    player_id: int
    tile: Tile

    def __repr__(self) -> str:
        return f"Moving player #{self.player_id} to {self.tile.name} at ({self.tile.x}, {self.tile.y})"


@dataclass(frozen=True)
class AdvShore:
    player_id: int
    tile: Tile

    def __repr__(self) -> str:
        return f"Player #{self.player_id} shores up {self.tile.name} at ({self.tile.x}, {self.tile.y})"


@dataclass(frozen=True)
class AdvPassCard:
    from_player_id: int
    from_player_card_idx: int
    to_player_id: int
    to_player_role: str
    card: TreasureCard

    def __repr__(self) -> str:
        return f"Player #{self.from_player_id} passes {self.card.name} to player #{self.to_player_id}"


@dataclass(frozen=True)
class AdvCollectTreasure:
    player_id: int
    treasure: Treasure

    def __repr__(self) -> str:
        return f"Player #{self.player_id} collects the {self.treasure.value}"


@dataclass(frozen=True)
class AdvPlaySandbags:
    player_id_turn: int
    card_owner_idx: int
    card_in_hand_idx: int
    tile: Tile

    def __repr__(self) -> str:
        return f"Player #{self.card_owner_idx}'s Sandbags shores up {self.tile} at ({self.tile.x}, {self.tile.y})"


@dataclass(frozen=True)
class AdvPlayHeliLift:
    player_id_turn: int
    card_owner_idx: int
    card_in_hand_idx: int
    player_roles_to_move: list[str]
    source_tile: Tile
    dest_tile: Tile

    def __repr__(self) -> str:
        player_str = ' and '.join([r for r in self.player_roles_to_move])
        return (f"Player #{self.card_owner_idx}'s Helicopter Lift moves {player_str} "
                f"from {self.source_tile.name} to {self.dest_tile.name}")


@dataclass(frozen=True)
class AdvDiscard:
    player_id: int
    card_in_hand_idx: int
    card: TreasureCard

    def __repr__(self) -> str:
        return f"Player #{self.player_id} discards {self.card.name}"


@dataclass(frozen=True)
class AdvEndTurn:
    player_id: int

    def __repr__(self) -> str:
        return f"Player #{self.player_id} passes the turn"
