from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MapperResponse")


@_attrs_define
class MapperResponse:
    """
    Attributes:
        id (Union[None, Unset, int]):
        player_id (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        avatar (Union[None, Unset, str]):
        curator (Union[None, Unset, bool]):
        verified_mapper (Union[Unset, bool]):
    """

    id: Union[None, Unset, int] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    avatar: Union[None, Unset, str] = UNSET
    curator: Union[None, Unset, bool] = UNSET
    verified_mapper: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id: Union[None, Unset, int]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

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

        curator: Union[None, Unset, bool]
        if isinstance(self.curator, Unset):
            curator = UNSET
        else:
            curator = self.curator

        verified_mapper = self.verified_mapper

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if name is not UNSET:
            field_dict["name"] = name
        if avatar is not UNSET:
            field_dict["avatar"] = avatar
        if curator is not UNSET:
            field_dict["curator"] = curator
        if verified_mapper is not UNSET:
            field_dict["verifiedMapper"] = verified_mapper

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_player_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_id = _parse_player_id(d.pop("playerId", UNSET))

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

        def _parse_curator(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        curator = _parse_curator(d.pop("curator", UNSET))

        verified_mapper = d.pop("verifiedMapper", UNSET)

        mapper_response = cls(
            id=id,
            player_id=player_id,
            name=name,
            avatar=avatar,
            curator=curator,
            verified_mapper=verified_mapper,
        )

        return mapper_response
