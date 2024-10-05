from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlayerFollower")


@_attrs_define
class PlayerFollower:
    """
    Attributes:
        id (Union[None, Unset, str]):
        alias (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        avatar (Union[None, Unset, str]):
        count (Union[None, Unset, int]):
        mutual (Union[Unset, bool]):
    """

    id: Union[None, Unset, str] = UNSET
    alias: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    avatar: Union[None, Unset, str] = UNSET
    count: Union[None, Unset, int] = UNSET
    mutual: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        alias: Union[None, Unset, str]
        if isinstance(self.alias, Unset):
            alias = UNSET
        else:
            alias = self.alias

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        avatar: Union[None, Unset, str]
        if isinstance(self.avatar, Unset):
            avatar = UNSET
        else:
            avatar = self.avatar

        count: Union[None, Unset, int]
        if isinstance(self.count, Unset):
            count = UNSET
        else:
            count = self.count

        mutual = self.mutual

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if alias is not UNSET:
            field_dict["alias"] = alias
        if name is not UNSET:
            field_dict["name"] = name
        if avatar is not UNSET:
            field_dict["avatar"] = avatar
        if count is not UNSET:
            field_dict["count"] = count
        if mutual is not UNSET:
            field_dict["mutual"] = mutual

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_alias(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        alias = _parse_alias(d.pop("alias", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_avatar(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        avatar = _parse_avatar(d.pop("avatar", UNSET))

        def _parse_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        count = _parse_count(d.pop("count", UNSET))

        mutual = d.pop("mutual", UNSET)

        player_follower = cls(
            id=id,
            alias=alias,
            name=name,
            avatar=avatar,
            count=count,
            mutual=mutual,
        )

        return player_follower
