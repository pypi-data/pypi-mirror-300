from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ClanMapConnection")


@_attrs_define
class ClanMapConnection:
    """
    Attributes:
        id (Union[None, Unset, int]):
        pp (Union[Unset, float]):
    """

    id: Union[None, Unset, int] = UNSET
    pp: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id: Union[None, Unset, int]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        pp = self.pp

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if pp is not UNSET:
            field_dict["pp"] = pp

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

        pp = d.pop("pp", UNSET)

        clan_map_connection = cls(
            id=id,
            pp=pp,
        )

        return clan_map_connection
