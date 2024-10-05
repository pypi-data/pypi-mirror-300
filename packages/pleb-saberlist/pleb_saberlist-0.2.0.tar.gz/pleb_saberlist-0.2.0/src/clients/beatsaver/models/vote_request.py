from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.auth_request import AuthRequest


T = TypeVar("T", bound="VoteRequest")


@_attrs_define
class VoteRequest:
    """
    Attributes:
        auth (Union[Unset, AuthRequest]):
        direction (Union[Unset, bool]):
        hash_ (Union[Unset, str]):
    """

    auth: Union[Unset, "AuthRequest"] = UNSET
    direction: Union[Unset, bool] = UNSET
    hash_: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        auth: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.auth, Unset):
            auth = self.auth.to_dict()

        direction = self.direction

        hash_ = self.hash_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auth is not UNSET:
            field_dict["auth"] = auth
        if direction is not UNSET:
            field_dict["direction"] = direction
        if hash_ is not UNSET:
            field_dict["hash"] = hash_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.auth_request import AuthRequest

        d = src_dict.copy()
        _auth = d.pop("auth", UNSET)
        auth: Union[Unset, AuthRequest]
        if isinstance(_auth, Unset):
            auth = UNSET
        else:
            auth = AuthRequest.from_dict(_auth)

        direction = d.pop("direction", UNSET)

        hash_ = d.pop("hash", UNSET)

        vote_request = cls(
            auth=auth,
            direction=direction,
            hash_=hash_,
        )

        vote_request.additional_properties = d
        return vote_request

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
