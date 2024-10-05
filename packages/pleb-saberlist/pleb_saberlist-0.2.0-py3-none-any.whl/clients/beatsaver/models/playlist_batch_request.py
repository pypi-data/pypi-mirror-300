from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlaylistBatchRequest")


@_attrs_define
class PlaylistBatchRequest:
    """
    Attributes:
        hashes (Union[Unset, List[str]]):
        ignore_unknown (Union[Unset, bool]):
        in_playlist (Union[Unset, bool]):
        keys (Union[Unset, List[str]]):
    """

    hashes: Union[Unset, List[str]] = UNSET
    ignore_unknown: Union[Unset, bool] = UNSET
    in_playlist: Union[Unset, bool] = UNSET
    keys: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        hashes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.hashes, Unset):
            hashes = self.hashes

        ignore_unknown = self.ignore_unknown

        in_playlist = self.in_playlist

        keys: Union[Unset, List[str]] = UNSET
        if not isinstance(self.keys, Unset):
            keys = self.keys

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hashes is not UNSET:
            field_dict["hashes"] = hashes
        if ignore_unknown is not UNSET:
            field_dict["ignoreUnknown"] = ignore_unknown
        if in_playlist is not UNSET:
            field_dict["inPlaylist"] = in_playlist
        if keys is not UNSET:
            field_dict["keys"] = keys

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        hashes = cast(List[str], d.pop("hashes", UNSET))

        ignore_unknown = d.pop("ignoreUnknown", UNSET)

        in_playlist = d.pop("inPlaylist", UNSET)

        keys = cast(List[str], d.pop("keys", UNSET))

        playlist_batch_request = cls(
            hashes=hashes,
            ignore_unknown=ignore_unknown,
            in_playlist=in_playlist,
            keys=keys,
        )

        playlist_batch_request.additional_properties = d
        return playlist_batch_request

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
