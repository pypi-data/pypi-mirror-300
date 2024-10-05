from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlayerChange")


@_attrs_define
class PlayerChange:
    """
    Attributes:
        id (Union[Unset, int]):
        timestamp (Union[Unset, int]):
        player_id (Union[None, Unset, str]):
        old_name (Union[None, Unset, str]):
        new_name (Union[None, Unset, str]):
        old_country (Union[None, Unset, str]):
        new_country (Union[None, Unset, str]):
        changer (Union[None, Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    timestamp: Union[Unset, int] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    old_name: Union[None, Unset, str] = UNSET
    new_name: Union[None, Unset, str] = UNSET
    old_country: Union[None, Unset, str] = UNSET
    new_country: Union[None, Unset, str] = UNSET
    changer: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        timestamp = self.timestamp

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        old_name: Union[None, Unset, str]
        if isinstance(self.old_name, Unset):
            old_name = UNSET
        else:
            old_name = self.old_name

        new_name: Union[None, Unset, str]
        if isinstance(self.new_name, Unset):
            new_name = UNSET
        else:
            new_name = self.new_name

        old_country: Union[None, Unset, str]
        if isinstance(self.old_country, Unset):
            old_country = UNSET
        else:
            old_country = self.old_country

        new_country: Union[None, Unset, str]
        if isinstance(self.new_country, Unset):
            new_country = UNSET
        else:
            new_country = self.new_country

        changer: Union[None, Unset, str]
        if isinstance(self.changer, Unset):
            changer = UNSET
        else:
            changer = self.changer

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if old_name is not UNSET:
            field_dict["oldName"] = old_name
        if new_name is not UNSET:
            field_dict["newName"] = new_name
        if old_country is not UNSET:
            field_dict["oldCountry"] = old_country
        if new_country is not UNSET:
            field_dict["newCountry"] = new_country
        if changer is not UNSET:
            field_dict["changer"] = changer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        def _parse_player_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_id = _parse_player_id(d.pop("playerId", UNSET))

        def _parse_old_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        old_name = _parse_old_name(d.pop("oldName", UNSET))

        def _parse_new_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        new_name = _parse_new_name(d.pop("newName", UNSET))

        def _parse_old_country(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        old_country = _parse_old_country(d.pop("oldCountry", UNSET))

        def _parse_new_country(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        new_country = _parse_new_country(d.pop("newCountry", UNSET))

        def _parse_changer(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        changer = _parse_changer(d.pop("changer", UNSET))

        player_change = cls(
            id=id,
            timestamp=timestamp,
            player_id=player_id,
            old_name=old_name,
            new_name=new_name,
            old_country=old_country,
            new_country=new_country,
            changer=changer,
        )

        return player_change
