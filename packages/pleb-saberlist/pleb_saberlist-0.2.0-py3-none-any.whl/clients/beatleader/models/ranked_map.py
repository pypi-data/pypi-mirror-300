from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RankedMap")


@_attrs_define
class RankedMap:
    """
    Attributes:
        name (Union[None, Unset, str]):
        song_id (Union[None, Unset, str]):
        cover (Union[None, Unset, str]):
        stars (Union[None, Unset, float]):
    """

    name: Union[None, Unset, str] = UNSET
    song_id: Union[None, Unset, str] = UNSET
    cover: Union[None, Unset, str] = UNSET
    stars: Union[None, Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        song_id: Union[None, Unset, str]
        if isinstance(self.song_id, Unset):
            song_id = UNSET
        else:
            song_id = self.song_id

        cover: Union[None, Unset, str]
        if isinstance(self.cover, Unset):
            cover = UNSET
        else:
            cover = self.cover

        stars: Union[None, Unset, float]
        if isinstance(self.stars, Unset):
            stars = UNSET
        else:
            stars = self.stars

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if song_id is not UNSET:
            field_dict["songId"] = song_id
        if cover is not UNSET:
            field_dict["cover"] = cover
        if stars is not UNSET:
            field_dict["stars"] = stars

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_song_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        song_id = _parse_song_id(d.pop("songId", UNSET))

        def _parse_cover(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cover = _parse_cover(d.pop("cover", UNSET))

        def _parse_stars(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        stars = _parse_stars(d.pop("stars", UNSET))

        ranked_map = cls(
            name=name,
            song_id=song_id,
            cover=cover,
            stars=stars,
        )

        return ranked_map
