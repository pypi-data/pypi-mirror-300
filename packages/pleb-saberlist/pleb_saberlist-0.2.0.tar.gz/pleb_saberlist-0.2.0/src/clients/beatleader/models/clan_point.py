from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ClanPoint")


@_attrs_define
class ClanPoint:
    """
    Attributes:
        id (Union[Unset, int]):
        tag (Union[None, Unset, str]):
        color (Union[None, Unset, str]):
        x (Union[Unset, float]):
        y (Union[Unset, float]):
    """

    id: Union[Unset, int] = UNSET
    tag: Union[None, Unset, str] = UNSET
    color: Union[None, Unset, str] = UNSET
    x: Union[Unset, float] = UNSET
    y: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        tag: Union[None, Unset, str]
        if isinstance(self.tag, Unset):
            tag = UNSET
        else:
            tag = self.tag

        color: Union[None, Unset, str]
        if isinstance(self.color, Unset):
            color = UNSET
        else:
            color = self.color

        x = self.x

        y = self.y

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if tag is not UNSET:
            field_dict["tag"] = tag
        if color is not UNSET:
            field_dict["color"] = color
        if x is not UNSET:
            field_dict["x"] = x
        if y is not UNSET:
            field_dict["y"] = y

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_tag(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tag = _parse_tag(d.pop("tag", UNSET))

        def _parse_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        color = _parse_color(d.pop("color", UNSET))

        x = d.pop("x", UNSET)

        y = d.pop("y", UNSET)

        clan_point = cls(
            id=id,
            tag=tag,
            color=color,
            x=x,
            y=y,
        )

        return clan_point
