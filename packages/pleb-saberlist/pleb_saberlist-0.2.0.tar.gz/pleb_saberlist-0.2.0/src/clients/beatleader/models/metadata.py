from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Metadata")


@_attrs_define
class Metadata:
    """
    Attributes:
        items_per_page (Union[Unset, int]):
        page (Union[Unset, int]):
        total (Union[Unset, int]):
    """

    items_per_page: Union[Unset, int] = UNSET
    page: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        items_per_page = self.items_per_page

        page = self.page

        total = self.total

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if items_per_page is not UNSET:
            field_dict["itemsPerPage"] = items_per_page
        if page is not UNSET:
            field_dict["page"] = page
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        items_per_page = d.pop("itemsPerPage", UNSET)

        page = d.pop("page", UNSET)

        total = d.pop("total", UNSET)

        metadata = cls(
            items_per_page=items_per_page,
            page=page,
            total=total,
        )

        return metadata
