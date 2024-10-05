from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.map_quality import MapQuality
from ..types import UNSET, Unset

T = TypeVar("T", bound="QualificationVote")


@_attrs_define
class QualificationVote:
    """
    Attributes:
        id (Union[Unset, int]):
        player_id (Union[None, Unset, str]):
        timeset (Union[Unset, int]):
        value (Union[Unset, MapQuality]):
        edit_timeset (Union[None, Unset, int]):
        edited (Union[Unset, bool]):
        rank_qualification_id (Union[None, Unset, int]):
        discord_rt_message_id (Union[None, Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    timeset: Union[Unset, int] = UNSET
    value: Union[Unset, MapQuality] = UNSET
    edit_timeset: Union[None, Unset, int] = UNSET
    edited: Union[Unset, bool] = UNSET
    rank_qualification_id: Union[None, Unset, int] = UNSET
    discord_rt_message_id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        timeset = self.timeset

        value: Union[Unset, str] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.value

        edit_timeset: Union[None, Unset, int]
        if isinstance(self.edit_timeset, Unset):
            edit_timeset = UNSET
        else:
            edit_timeset = self.edit_timeset

        edited = self.edited

        rank_qualification_id: Union[None, Unset, int]
        if isinstance(self.rank_qualification_id, Unset):
            rank_qualification_id = UNSET
        else:
            rank_qualification_id = self.rank_qualification_id

        discord_rt_message_id: Union[None, Unset, str]
        if isinstance(self.discord_rt_message_id, Unset):
            discord_rt_message_id = UNSET
        else:
            discord_rt_message_id = self.discord_rt_message_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if timeset is not UNSET:
            field_dict["timeset"] = timeset
        if value is not UNSET:
            field_dict["value"] = value
        if edit_timeset is not UNSET:
            field_dict["editTimeset"] = edit_timeset
        if edited is not UNSET:
            field_dict["edited"] = edited
        if rank_qualification_id is not UNSET:
            field_dict["rankQualificationId"] = rank_qualification_id
        if discord_rt_message_id is not UNSET:
            field_dict["discordRTMessageId"] = discord_rt_message_id

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

        timeset = d.pop("timeset", UNSET)

        _value = d.pop("value", UNSET)
        value: Union[Unset, MapQuality]
        if isinstance(_value, Unset):
            value = UNSET
        else:
            value = MapQuality(_value)

        def _parse_edit_timeset(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        edit_timeset = _parse_edit_timeset(d.pop("editTimeset", UNSET))

        edited = d.pop("edited", UNSET)

        def _parse_rank_qualification_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        rank_qualification_id = _parse_rank_qualification_id(d.pop("rankQualificationId", UNSET))

        def _parse_discord_rt_message_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        discord_rt_message_id = _parse_discord_rt_message_id(d.pop("discordRTMessageId", UNSET))

        qualification_vote = cls(
            id=id,
            player_id=player_id,
            timeset=timeset,
            value=value,
            edit_timeset=edit_timeset,
            edited=edited,
            rank_qualification_id=rank_qualification_id,
            discord_rt_message_id=discord_rt_message_id,
        )

        return qualification_vote
