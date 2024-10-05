from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CompactLeaderboard")


@_attrs_define
class CompactLeaderboard:
    """
    Attributes:
        id (Union[None, Unset, str]):
        song_hash (Union[None, Unset, str]):
        mode_name (Union[None, Unset, str]):
        difficulty (Union[Unset, int]):
    """

    id: Union[None, Unset, str] = UNSET
    song_hash: Union[None, Unset, str] = UNSET
    mode_name: Union[None, Unset, str] = UNSET
    difficulty: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        song_hash: Union[None, Unset, str]
        if isinstance(self.song_hash, Unset):
            song_hash = UNSET
        else:
            song_hash = self.song_hash

        mode_name: Union[None, Unset, str]
        if isinstance(self.mode_name, Unset):
            mode_name = UNSET
        else:
            mode_name = self.mode_name

        difficulty = self.difficulty

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if song_hash is not UNSET:
            field_dict["songHash"] = song_hash
        if mode_name is not UNSET:
            field_dict["modeName"] = mode_name
        if difficulty is not UNSET:
            field_dict["difficulty"] = difficulty

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_song_hash(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        song_hash = _parse_song_hash(d.pop("songHash", UNSET))

        def _parse_mode_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mode_name = _parse_mode_name(d.pop("modeName", UNSET))

        difficulty = d.pop("difficulty", UNSET)

        compact_leaderboard = cls(
            id=id,
            song_hash=song_hash,
            mode_name=mode_name,
            difficulty=difficulty,
        )

        return compact_leaderboard
