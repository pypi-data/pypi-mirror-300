from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ClanBiggerResponse")


@_attrs_define
class ClanBiggerResponse:
    """
    Attributes:
        id (Union[Unset, int]):
        tag (Union[None, Unset, str]):
        color (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        icon (Union[None, Unset, str]):
        ranked_pool_percent_captured (Union[Unset, float]):
        players_count (Union[Unset, int]):
        joined (Union[Unset, bool]):
    """

    id: Union[Unset, int] = UNSET
    tag: Union[None, Unset, str] = UNSET
    color: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    icon: Union[None, Unset, str] = UNSET
    ranked_pool_percent_captured: Union[Unset, float] = UNSET
    players_count: Union[Unset, int] = UNSET
    joined: Union[Unset, bool] = UNSET

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

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        icon: Union[None, Unset, str]
        if isinstance(self.icon, Unset):
            icon = UNSET
        else:
            icon = self.icon

        ranked_pool_percent_captured = self.ranked_pool_percent_captured

        players_count = self.players_count

        joined = self.joined

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if tag is not UNSET:
            field_dict["tag"] = tag
        if color is not UNSET:
            field_dict["color"] = color
        if name is not UNSET:
            field_dict["name"] = name
        if icon is not UNSET:
            field_dict["icon"] = icon
        if ranked_pool_percent_captured is not UNSET:
            field_dict["rankedPoolPercentCaptured"] = ranked_pool_percent_captured
        if players_count is not UNSET:
            field_dict["playersCount"] = players_count
        if joined is not UNSET:
            field_dict["joined"] = joined

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

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_icon(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        icon = _parse_icon(d.pop("icon", UNSET))

        ranked_pool_percent_captured = d.pop("rankedPoolPercentCaptured", UNSET)

        players_count = d.pop("playersCount", UNSET)

        joined = d.pop("joined", UNSET)

        clan_bigger_response = cls(
            id=id,
            tag=tag,
            color=color,
            name=name,
            icon=icon,
            ranked_pool_percent_captured=ranked_pool_percent_captured,
            players_count=players_count,
            joined=joined,
        )

        return clan_bigger_response
