from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="LeaderboardPlayer")


@_attrs_define
class LeaderboardPlayer:
    """
    Attributes:
        id (str):
        name (str):
        profile_picture (str):
        country (str):
        permissions (float):
        role (str):
    """

    id: str
    name: str
    profile_picture: str
    country: str
    permissions: float
    role: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        profile_picture = self.profile_picture

        country = self.country

        permissions = self.permissions

        role = self.role

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "profilePicture": profile_picture,
                "country": country,
                "permissions": permissions,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        profile_picture = d.pop("profilePicture")

        country = d.pop("country")

        permissions = d.pop("permissions")

        role = d.pop("role")

        leaderboard_player = cls(
            id=id,
            name=name,
            profile_picture=profile_picture,
            country=country,
            permissions=permissions,
            role=role,
        )

        return leaderboard_player
