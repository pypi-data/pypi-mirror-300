from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MapParitySummary")


@_attrs_define
class MapParitySummary:
    """
    Attributes:
        errors (Union[Unset, int]):
        resets (Union[Unset, int]):
        warns (Union[Unset, int]):
    """

    errors: Union[Unset, int] = UNSET
    resets: Union[Unset, int] = UNSET
    warns: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        errors = self.errors

        resets = self.resets

        warns = self.warns

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if errors is not UNSET:
            field_dict["errors"] = errors
        if resets is not UNSET:
            field_dict["resets"] = resets
        if warns is not UNSET:
            field_dict["warns"] = warns

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        errors = d.pop("errors", UNSET)

        resets = d.pop("resets", UNSET)

        warns = d.pop("warns", UNSET)

        map_parity_summary = cls(
            errors=errors,
            resets=resets,
            warns=warns,
        )

        map_parity_summary.additional_properties = d
        return map_parity_summary

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
