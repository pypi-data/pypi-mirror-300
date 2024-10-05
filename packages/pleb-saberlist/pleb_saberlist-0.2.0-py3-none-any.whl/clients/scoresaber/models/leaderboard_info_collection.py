from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.leaderboard_info import LeaderboardInfo
    from ..models.metadata import Metadata


T = TypeVar("T", bound="LeaderboardInfoCollection")


@_attrs_define
class LeaderboardInfoCollection:
    """
    Attributes:
        leaderboards (List['LeaderboardInfo']):
        metadata (Metadata):
    """

    leaderboards: List["LeaderboardInfo"]
    metadata: "Metadata"

    def to_dict(self) -> Dict[str, Any]:
        leaderboards = []
        for leaderboards_item_data in self.leaderboards:
            leaderboards_item = leaderboards_item_data.to_dict()
            leaderboards.append(leaderboards_item)

        metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "leaderboards": leaderboards,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.leaderboard_info import LeaderboardInfo
        from ..models.metadata import Metadata

        d = src_dict.copy()
        leaderboards = []
        _leaderboards = d.pop("leaderboards")
        for leaderboards_item_data in _leaderboards:
            leaderboards_item = LeaderboardInfo.from_dict(leaderboards_item_data)

            leaderboards.append(leaderboards_item)

        metadata = Metadata.from_dict(d.pop("metadata"))

        leaderboard_info_collection = cls(
            leaderboards=leaderboards,
            metadata=metadata,
        )

        return leaderboard_info_collection
