from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MapDetailMetadata")


@_attrs_define
class MapDetailMetadata:
    """
    Attributes:
        bpm (Union[Unset, Any]):
        duration (Union[Unset, int]):
        level_author_name (Union[Unset, str]):
        song_author_name (Union[Unset, str]):
        song_name (Union[Unset, str]):
        song_sub_name (Union[Unset, str]):
    """

    bpm: Union[Unset, Any] = UNSET
    duration: Union[Unset, int] = UNSET
    level_author_name: Union[Unset, str] = UNSET
    song_author_name: Union[Unset, str] = UNSET
    song_name: Union[Unset, str] = UNSET
    song_sub_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bpm = self.bpm

        duration = self.duration

        level_author_name = self.level_author_name

        song_author_name = self.song_author_name

        song_name = self.song_name

        song_sub_name = self.song_sub_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bpm is not UNSET:
            field_dict["bpm"] = bpm
        if duration is not UNSET:
            field_dict["duration"] = duration
        if level_author_name is not UNSET:
            field_dict["levelAuthorName"] = level_author_name
        if song_author_name is not UNSET:
            field_dict["songAuthorName"] = song_author_name
        if song_name is not UNSET:
            field_dict["songName"] = song_name
        if song_sub_name is not UNSET:
            field_dict["songSubName"] = song_sub_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bpm = d.pop("bpm", UNSET)

        duration = d.pop("duration", UNSET)

        level_author_name = d.pop("levelAuthorName", UNSET)

        song_author_name = d.pop("songAuthorName", UNSET)

        song_name = d.pop("songName", UNSET)

        song_sub_name = d.pop("songSubName", UNSET)

        map_detail_metadata = cls(
            bpm=bpm,
            duration=duration,
            level_author_name=level_author_name,
            song_author_name=song_author_name,
            song_name=song_name,
            song_sub_name=song_sub_name,
        )

        map_detail_metadata.additional_properties = d
        return map_detail_metadata

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
