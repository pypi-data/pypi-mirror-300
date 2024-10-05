from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlayerSocial")


@_attrs_define
class PlayerSocial:
    """
    Attributes:
        id (Union[Unset, int]):
        service (Union[None, Unset, str]):
        link (Union[None, Unset, str]):
        user (Union[None, Unset, str]):
        user_id (Union[None, Unset, str]):
        player_id (Union[None, Unset, str]):
        hidden (Union[Unset, bool]):
    """

    id: Union[Unset, int] = UNSET
    service: Union[None, Unset, str] = UNSET
    link: Union[None, Unset, str] = UNSET
    user: Union[None, Unset, str] = UNSET
    user_id: Union[None, Unset, str] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    hidden: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        service: Union[None, Unset, str]
        if isinstance(self.service, Unset):
            service = UNSET
        else:
            service = self.service

        link: Union[None, Unset, str]
        if isinstance(self.link, Unset):
            link = UNSET
        else:
            link = self.link

        user: Union[None, Unset, str]
        if isinstance(self.user, Unset):
            user = UNSET
        else:
            user = self.user

        user_id: Union[None, Unset, str]
        if isinstance(self.user_id, Unset):
            user_id = UNSET
        else:
            user_id = self.user_id

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        hidden = self.hidden

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if service is not UNSET:
            field_dict["service"] = service
        if link is not UNSET:
            field_dict["link"] = link
        if user is not UNSET:
            field_dict["user"] = user
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if hidden is not UNSET:
            field_dict["hidden"] = hidden

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_service(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        service = _parse_service(d.pop("service", UNSET))

        def _parse_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        link = _parse_link(d.pop("link", UNSET))

        def _parse_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user = _parse_user(d.pop("user", UNSET))

        def _parse_user_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_id = _parse_user_id(d.pop("userId", UNSET))

        def _parse_player_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_id = _parse_player_id(d.pop("playerId", UNSET))

        hidden = d.pop("hidden", UNSET)

        player_social = cls(
            id=id,
            service=service,
            link=link,
            user=user,
            user_id=user_id,
            player_id=player_id,
            hidden=hidden,
        )

        return player_social
