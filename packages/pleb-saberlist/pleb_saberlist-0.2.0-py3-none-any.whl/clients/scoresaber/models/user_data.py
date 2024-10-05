from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UserData")


@_attrs_define
class UserData:
    """
    Attributes:
        player_id (str):
        permissions (float):
        quest_key (str):
    """

    player_id: str
    permissions: float
    quest_key: str

    def to_dict(self) -> Dict[str, Any]:
        player_id = self.player_id

        permissions = self.permissions

        quest_key = self.quest_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "playerId": player_id,
                "permissions": permissions,
                "questKey": quest_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        player_id = d.pop("playerId")

        permissions = d.pop("permissions")

        quest_key = d.pop("questKey")

        user_data = cls(
            player_id=player_id,
            permissions=permissions,
            quest_key=quest_key,
        )

        return user_data
