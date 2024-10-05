from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserFollowData")


@_attrs_define
class UserFollowData:
    """
    Attributes:
        collab (Union[Unset, bool]):
        curation (Union[Unset, bool]):
        followers (Union[Unset, int]):
        following (Union[Unset, bool]):
        follows (Union[Unset, int]):
        upload (Union[Unset, bool]):
    """

    collab: Union[Unset, bool] = UNSET
    curation: Union[Unset, bool] = UNSET
    followers: Union[Unset, int] = UNSET
    following: Union[Unset, bool] = UNSET
    follows: Union[Unset, int] = UNSET
    upload: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collab = self.collab

        curation = self.curation

        followers = self.followers

        following = self.following

        follows = self.follows

        upload = self.upload

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if collab is not UNSET:
            field_dict["collab"] = collab
        if curation is not UNSET:
            field_dict["curation"] = curation
        if followers is not UNSET:
            field_dict["followers"] = followers
        if following is not UNSET:
            field_dict["following"] = following
        if follows is not UNSET:
            field_dict["follows"] = follows
        if upload is not UNSET:
            field_dict["upload"] = upload

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        collab = d.pop("collab", UNSET)

        curation = d.pop("curation", UNSET)

        followers = d.pop("followers", UNSET)

        following = d.pop("following", UNSET)

        follows = d.pop("follows", UNSET)

        upload = d.pop("upload", UNSET)

        user_follow_data = cls(
            collab=collab,
            curation=curation,
            followers=followers,
            following=following,
            follows=follows,
            upload=upload,
        )

        user_follow_data.additional_properties = d
        return user_follow_data

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
