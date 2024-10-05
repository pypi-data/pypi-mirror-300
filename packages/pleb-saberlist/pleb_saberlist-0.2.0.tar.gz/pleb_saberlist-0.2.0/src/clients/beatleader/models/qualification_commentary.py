from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="QualificationCommentary")


@_attrs_define
class QualificationCommentary:
    """
    Attributes:
        id (Union[Unset, int]):
        player_id (Union[None, Unset, str]):
        timeset (Union[Unset, int]):
        value (Union[None, Unset, str]):
        edit_timeset (Union[None, Unset, int]):
        edited (Union[Unset, bool]):
        rank_qualification_id (Union[None, Unset, int]):
        discord_message_id (Union[None, Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    timeset: Union[Unset, int] = UNSET
    value: Union[None, Unset, str] = UNSET
    edit_timeset: Union[None, Unset, int] = UNSET
    edited: Union[Unset, bool] = UNSET
    rank_qualification_id: Union[None, Unset, int] = UNSET
    discord_message_id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        timeset = self.timeset

        value: Union[None, Unset, str]
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

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

        discord_message_id: Union[None, Unset, str]
        if isinstance(self.discord_message_id, Unset):
            discord_message_id = UNSET
        else:
            discord_message_id = self.discord_message_id

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
        if discord_message_id is not UNSET:
            field_dict["discordMessageId"] = discord_message_id

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

        def _parse_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        value = _parse_value(d.pop("value", UNSET))

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

        def _parse_discord_message_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        discord_message_id = _parse_discord_message_id(d.pop("discordMessageId", UNSET))

        qualification_commentary = cls(
            id=id,
            player_id=player_id,
            timeset=timeset,
            value=value,
            edit_timeset=edit_timeset,
            edited=edited,
            rank_qualification_id=rank_qualification_id,
            discord_message_id=discord_message_id,
        )

        return qualification_commentary
