from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="Metadata")


@_attrs_define
class Metadata:
    """
    Attributes:
        total (float):
        page (float):
        items_per_page (float):
    """

    total: float
    page: float
    items_per_page: float

    def to_dict(self) -> Dict[str, Any]:
        total = self.total

        page = self.page

        items_per_page = self.items_per_page

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "total": total,
                "page": page,
                "itemsPerPage": items_per_page,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total = d.pop("total")

        page = d.pop("page")

        items_per_page = d.pop("itemsPerPage")

        metadata = cls(
            total=total,
            page=page,
            items_per_page=items_per_page,
        )

        return metadata
