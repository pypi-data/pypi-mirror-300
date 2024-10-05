from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="BeastiesNomination")


@_attrs_define
class BeastiesNomination:
    """
    Attributes:
        id (Union[Unset, int]):
        player_id (Union[None, Unset, str]):
        leaderboard_id (Union[None, Unset, str]):
        category (Union[None, Unset, str]):
        timepost (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    leaderboard_id: Union[None, Unset, str] = UNSET
    category: Union[None, Unset, str] = UNSET
    timepost: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        leaderboard_id: Union[None, Unset, str]
        if isinstance(self.leaderboard_id, Unset):
            leaderboard_id = UNSET
        else:
            leaderboard_id = self.leaderboard_id

        category: Union[None, Unset, str]
        if isinstance(self.category, Unset):
            category = UNSET
        else:
            category = self.category

        timepost = self.timepost

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if leaderboard_id is not UNSET:
            field_dict["leaderboardId"] = leaderboard_id
        if category is not UNSET:
            field_dict["category"] = category
        if timepost is not UNSET:
            field_dict["timepost"] = timepost

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_player_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_id = _parse_player_id(d.pop("playerId", UNSET))

        def _parse_leaderboard_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        leaderboard_id = _parse_leaderboard_id(d.pop("leaderboardId", UNSET))

        def _parse_category(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        category = _parse_category(d.pop("category", UNSET))

        timepost = d.pop("timepost", UNSET)

        beasties_nomination = cls(
            id=id,
            player_id=player_id,
            leaderboard_id=leaderboard_id,
            category=category,
            timepost=timepost,
        )

        return beasties_nomination
