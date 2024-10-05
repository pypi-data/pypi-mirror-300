from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Ban")


@_attrs_define
class Ban:
    """
    Attributes:
        id (Union[Unset, int]):
        player_id (Union[None, Unset, str]):
        banned_by (Union[None, Unset, str]):
        ban_reason (Union[None, Unset, str]):
        timeset (Union[Unset, int]):
        duration (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    banned_by: Union[None, Unset, str] = UNSET
    ban_reason: Union[None, Unset, str] = UNSET
    timeset: Union[Unset, int] = UNSET
    duration: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        banned_by: Union[None, Unset, str]
        if isinstance(self.banned_by, Unset):
            banned_by = UNSET
        else:
            banned_by = self.banned_by

        ban_reason: Union[None, Unset, str]
        if isinstance(self.ban_reason, Unset):
            ban_reason = UNSET
        else:
            ban_reason = self.ban_reason

        timeset = self.timeset

        duration = self.duration

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if banned_by is not UNSET:
            field_dict["bannedBy"] = banned_by
        if ban_reason is not UNSET:
            field_dict["banReason"] = ban_reason
        if timeset is not UNSET:
            field_dict["timeset"] = timeset
        if duration is not UNSET:
            field_dict["duration"] = duration

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

        def _parse_banned_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        banned_by = _parse_banned_by(d.pop("bannedBy", UNSET))

        def _parse_ban_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ban_reason = _parse_ban_reason(d.pop("banReason", UNSET))

        timeset = d.pop("timeset", UNSET)

        duration = d.pop("duration", UNSET)

        ban = cls(
            id=id,
            player_id=player_id,
            banned_by=banned_by,
            ban_reason=ban_reason,
            timeset=timeset,
            duration=duration,
        )

        return ban
