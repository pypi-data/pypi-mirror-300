from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="Badge")


@_attrs_define
class Badge:
    """
    Attributes:
        description (str):
        image (str):
    """

    description: str
    image: str

    def to_dict(self) -> Dict[str, Any]:
        description = self.description

        image = self.image

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "description": description,
                "image": image,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description")

        image = d.pop("image")

        badge = cls(
            description=description,
            image=image,
        )

        return badge
