from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.player import Player


T = TypeVar("T", bound="PlayerSearch")


@_attrs_define
class PlayerSearch:
    """
    Attributes:
        id (Union[Unset, int]):
        score (Union[Unset, int]):
        search_id (Union[Unset, int]):
        player_id (Union[None, Unset, str]):
        player (Union[Unset, Player]):
    """

    id: Union[Unset, int] = UNSET
    score: Union[Unset, int] = UNSET
    search_id: Union[Unset, int] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    player: Union[Unset, "Player"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        score = self.score

        search_id = self.search_id

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        player: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.player, Unset):
            player = self.player.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if score is not UNSET:
            field_dict["score"] = score
        if search_id is not UNSET:
            field_dict["searchId"] = search_id
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if player is not UNSET:
            field_dict["player"] = player

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.player import Player

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        score = d.pop("score", UNSET)

        search_id = d.pop("searchId", UNSET)

        def _parse_player_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_id = _parse_player_id(d.pop("playerId", UNSET))

        _player = d.pop("player", UNSET)
        player: Union[Unset, Player]
        if isinstance(_player, Unset):
            player = UNSET
        else:
            player = Player.from_dict(_player)

        player_search = cls(
            id=id,
            score=score,
            search_id=search_id,
            player_id=player_id,
            player=player,
        )

        return player_search
