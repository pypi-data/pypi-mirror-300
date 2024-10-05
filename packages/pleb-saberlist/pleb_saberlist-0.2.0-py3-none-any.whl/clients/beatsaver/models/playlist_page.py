from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.map_detail_with_order import MapDetailWithOrder
    from ..models.playlist_full import PlaylistFull


T = TypeVar("T", bound="PlaylistPage")


@_attrs_define
class PlaylistPage:
    """
    Attributes:
        maps (Union[Unset, List['MapDetailWithOrder']]):
        playlist (Union[Unset, PlaylistFull]):
    """

    maps: Union[Unset, List["MapDetailWithOrder"]] = UNSET
    playlist: Union[Unset, "PlaylistFull"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        maps: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.maps, Unset):
            maps = []
            for maps_item_data in self.maps:
                maps_item = maps_item_data.to_dict()
                maps.append(maps_item)

        playlist: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.playlist, Unset):
            playlist = self.playlist.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if maps is not UNSET:
            field_dict["maps"] = maps
        if playlist is not UNSET:
            field_dict["playlist"] = playlist

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.map_detail_with_order import MapDetailWithOrder
        from ..models.playlist_full import PlaylistFull

        d = src_dict.copy()
        maps = []
        _maps = d.pop("maps", UNSET)
        for maps_item_data in _maps or []:
            maps_item = MapDetailWithOrder.from_dict(maps_item_data)

            maps.append(maps_item)

        _playlist = d.pop("playlist", UNSET)
        playlist: Union[Unset, PlaylistFull]
        if isinstance(_playlist, Unset):
            playlist = UNSET
        else:
            playlist = PlaylistFull.from_dict(_playlist)

        playlist_page = cls(
            maps=maps,
            playlist=playlist,
        )

        playlist_page.additional_properties = d
        return playlist_page

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
