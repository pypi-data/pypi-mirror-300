from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.leaderboard_info import LeaderboardInfo
    from ..models.vote_group import VoteGroup


T = TypeVar("T", bound="RankRequestListing")


@_attrs_define
class RankRequestListing:
    """
    Attributes:
        request_id (float):
        weight (float):
        leaderboard_info (LeaderboardInfo):
        created_at (str):
        total_rank_votes (VoteGroup):
        total_qat_votes (VoteGroup):
        difficulty_count (float):
    """

    request_id: float
    weight: float
    leaderboard_info: "LeaderboardInfo"
    created_at: str
    total_rank_votes: "VoteGroup"
    total_qat_votes: "VoteGroup"
    difficulty_count: float

    def to_dict(self) -> Dict[str, Any]:
        request_id = self.request_id

        weight = self.weight

        leaderboard_info = self.leaderboard_info.to_dict()

        created_at = self.created_at

        total_rank_votes = self.total_rank_votes.to_dict()

        total_qat_votes = self.total_qat_votes.to_dict()

        difficulty_count = self.difficulty_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "requestId": request_id,
                "weight": weight,
                "leaderboardInfo": leaderboard_info,
                "created_at": created_at,
                "totalRankVotes": total_rank_votes,
                "totalQATVotes": total_qat_votes,
                "difficultyCount": difficulty_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.leaderboard_info import LeaderboardInfo
        from ..models.vote_group import VoteGroup

        d = src_dict.copy()
        request_id = d.pop("requestId")

        weight = d.pop("weight")

        leaderboard_info = LeaderboardInfo.from_dict(d.pop("leaderboardInfo"))

        created_at = d.pop("created_at")

        total_rank_votes = VoteGroup.from_dict(d.pop("totalRankVotes"))

        total_qat_votes = VoteGroup.from_dict(d.pop("totalQATVotes"))

        difficulty_count = d.pop("difficultyCount")

        rank_request_listing = cls(
            request_id=request_id,
            weight=weight,
            leaderboard_info=leaderboard_info,
            created_at=created_at,
            total_rank_votes=total_rank_votes,
            total_qat_votes=total_qat_votes,
            difficulty_count=difficulty_count,
        )

        return rank_request_listing
