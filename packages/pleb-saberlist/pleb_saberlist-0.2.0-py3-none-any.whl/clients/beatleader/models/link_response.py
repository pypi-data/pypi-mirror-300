from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="LinkResponse")


@_attrs_define
class LinkResponse:
    """
    Attributes:
        quest_id (Union[None, Unset, int]):
        steam_id (Union[None, Unset, str]):
        oculus_pc_id (Union[None, Unset, str]):
    """

    quest_id: Union[None, Unset, int] = UNSET
    steam_id: Union[None, Unset, str] = UNSET
    oculus_pc_id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        quest_id: Union[None, Unset, int]
        if isinstance(self.quest_id, Unset):
            quest_id = UNSET
        else:
            quest_id = self.quest_id

        steam_id: Union[None, Unset, str]
        if isinstance(self.steam_id, Unset):
            steam_id = UNSET
        else:
            steam_id = self.steam_id

        oculus_pc_id: Union[None, Unset, str]
        if isinstance(self.oculus_pc_id, Unset):
            oculus_pc_id = UNSET
        else:
            oculus_pc_id = self.oculus_pc_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if quest_id is not UNSET:
            field_dict["questId"] = quest_id
        if steam_id is not UNSET:
            field_dict["steamId"] = steam_id
        if oculus_pc_id is not UNSET:
            field_dict["oculusPCId"] = oculus_pc_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_quest_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        quest_id = _parse_quest_id(d.pop("questId", UNSET))

        def _parse_steam_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        steam_id = _parse_steam_id(d.pop("steamId", UNSET))

        def _parse_oculus_pc_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        oculus_pc_id = _parse_oculus_pc_id(d.pop("oculusPCId", UNSET))

        link_response = cls(
            quest_id=quest_id,
            steam_id=steam_id,
            oculus_pc_id=oculus_pc_id,
        )

        return link_response
