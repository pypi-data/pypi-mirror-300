from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Badge")


@_attrs_define
class Badge:
    """
    Attributes:
        id (Union[Unset, int]):
        description (Union[None, Unset, str]):
        image (Union[None, Unset, str]):
        link (Union[None, Unset, str]):
        timeset (Union[Unset, int]):
        hidden (Union[Unset, bool]):
    """

    id: Union[Unset, int] = UNSET
    description: Union[None, Unset, str] = UNSET
    image: Union[None, Unset, str] = UNSET
    link: Union[None, Unset, str] = UNSET
    timeset: Union[Unset, int] = UNSET
    hidden: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        link: Union[None, Unset, str]
        if isinstance(self.link, Unset):
            link = UNSET
        else:
            link = self.link

        timeset = self.timeset

        hidden = self.hidden

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if description is not UNSET:
            field_dict["description"] = description
        if image is not UNSET:
            field_dict["image"] = image
        if link is not UNSET:
            field_dict["link"] = link
        if timeset is not UNSET:
            field_dict["timeset"] = timeset
        if hidden is not UNSET:
            field_dict["hidden"] = hidden

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        def _parse_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        link = _parse_link(d.pop("link", UNSET))

        timeset = d.pop("timeset", UNSET)

        hidden = d.pop("hidden", UNSET)

        badge = cls(
            id=id,
            description=description,
            image=image,
            link=link,
            timeset=timeset,
            hidden=hidden,
        )

        return badge
