from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.player import Player


T = TypeVar("T", bound="PlayerCollection")


@_attrs_define
class PlayerCollection:
    """
    Attributes:
        players (List['Player']):
        metadata (Metadata):
    """

    players: List["Player"]
    metadata: "Metadata"

    def to_dict(self) -> Dict[str, Any]:
        players = []
        for players_item_data in self.players:
            players_item = players_item_data.to_dict()
            players.append(players_item)

        metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "players": players,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metadata import Metadata
        from ..models.player import Player

        d = src_dict.copy()
        players = []
        _players = d.pop("players")
        for players_item_data in _players:
            players_item = Player.from_dict(players_item_data)

            players.append(players_item)

        metadata = Metadata.from_dict(d.pop("metadata"))

        player_collection = cls(
            players=players,
            metadata=metadata,
        )

        return player_collection
