from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.difficulty_status import DifficultyStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="LeaderboardGroupEntry")


@_attrs_define
class LeaderboardGroupEntry:
    """
    Attributes:
        id (Union[None, Unset, str]):
        status (Union[Unset, DifficultyStatus]): Represents the difficulty status of a map.
        timestamp (Union[Unset, int]):
    """

    id: Union[None, Unset, str] = UNSET
    status: Union[Unset, DifficultyStatus] = UNSET
    timestamp: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        timestamp = self.timestamp

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

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

        _status = d.pop("status", UNSET)
        status: Union[Unset, DifficultyStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = DifficultyStatus(_status)

        timestamp = d.pop("timestamp", UNSET)

        leaderboard_group_entry = cls(
            id=id,
            status=status,
            timestamp=timestamp,
        )

        return leaderboard_group_entry
