from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NatReplaceBody")


@_attrs_define
class NatReplaceBody:
    """
    Attributes:
        request_id (float): The requestId affected
        leaderboard_id (float): The leaderboardId to replace the current requests leaderboardId
        description (str): An updated description
    """

    request_id: float
    leaderboard_id: float
    description: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_id = self.request_id

        leaderboard_id = self.leaderboard_id

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestId": request_id,
                "leaderboardId": leaderboard_id,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_id = d.pop("requestId")

        leaderboard_id = d.pop("leaderboardId")

        description = d.pop("description")

        nat_replace_body = cls(
            request_id=request_id,
            leaderboard_id=leaderboard_id,
            description=description,
        )

        nat_replace_body.additional_properties = d
        return nat_replace_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
