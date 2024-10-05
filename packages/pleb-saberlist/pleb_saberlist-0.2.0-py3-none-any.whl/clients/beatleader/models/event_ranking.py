from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="EventRanking")


@_attrs_define
class EventRanking:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[None, Unset, str]):
        end_date (Union[Unset, int]):
        playlist_id (Union[Unset, int]):
        image (Union[None, Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[None, Unset, str] = UNSET
    end_date: Union[Unset, int] = UNSET
    playlist_id: Union[Unset, int] = UNSET
    image: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        end_date = self.end_date

        playlist_id = self.playlist_id

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if playlist_id is not UNSET:
            field_dict["playlistId"] = playlist_id
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        end_date = d.pop("endDate", UNSET)

        playlist_id = d.pop("playlistId", UNSET)

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        event_ranking = cls(
            id=id,
            name=name,
            end_date=end_date,
            playlist_id=playlist_id,
            image=image,
        )

        return event_ranking
