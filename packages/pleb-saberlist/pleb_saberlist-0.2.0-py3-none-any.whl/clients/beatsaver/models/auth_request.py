from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthRequest")


@_attrs_define
class AuthRequest:
    """
    Attributes:
        oculus_id (Union[Unset, str]):
        proof (Union[Unset, str]):
        steam_id (Union[Unset, str]):
    """

    oculus_id: Union[Unset, str] = UNSET
    proof: Union[Unset, str] = UNSET
    steam_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        oculus_id = self.oculus_id

        proof = self.proof

        steam_id = self.steam_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if oculus_id is not UNSET:
            field_dict["oculusId"] = oculus_id
        if proof is not UNSET:
            field_dict["proof"] = proof
        if steam_id is not UNSET:
            field_dict["steamId"] = steam_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        oculus_id = d.pop("oculusId", UNSET)

        proof = d.pop("proof", UNSET)

        steam_id = d.pop("steamId", UNSET)

        auth_request = cls(
            oculus_id=oculus_id,
            proof=proof,
            steam_id=steam_id,
        )

        auth_request.additional_properties = d
        return auth_request

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
