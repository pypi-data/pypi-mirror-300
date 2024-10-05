from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.comment import Comment
    from ..models.leaderboard_info import LeaderboardInfo
    from ..models.ranking_difficulty import RankingDifficulty
    from ..models.vote_group import VoteGroup


T = TypeVar("T", bound="RankRequestInformation")


@_attrs_define
class RankRequestInformation:
    """
    Attributes:
        request_id (float):
        request_description (str):
        leaderboard_info (LeaderboardInfo):
        created_at (str):
        rank_votes (VoteGroup):
        qat_votes (VoteGroup):
        rank_comments (List['Comment']):
        qat_comments (List['Comment']):
        request_type (float):
        approved (float):
        difficulties (List['RankingDifficulty']):
    """

    request_id: float
    request_description: str
    leaderboard_info: "LeaderboardInfo"
    created_at: str
    rank_votes: "VoteGroup"
    qat_votes: "VoteGroup"
    rank_comments: List["Comment"]
    qat_comments: List["Comment"]
    request_type: float
    approved: float
    difficulties: List["RankingDifficulty"]

    def to_dict(self) -> Dict[str, Any]:
        request_id = self.request_id

        request_description = self.request_description

        leaderboard_info = self.leaderboard_info.to_dict()

        created_at = self.created_at

        rank_votes = self.rank_votes.to_dict()

        qat_votes = self.qat_votes.to_dict()

        rank_comments = []
        for rank_comments_item_data in self.rank_comments:
            rank_comments_item = rank_comments_item_data.to_dict()
            rank_comments.append(rank_comments_item)

        qat_comments = []
        for qat_comments_item_data in self.qat_comments:
            qat_comments_item = qat_comments_item_data.to_dict()
            qat_comments.append(qat_comments_item)

        request_type = self.request_type

        approved = self.approved

        difficulties = []
        for difficulties_item_data in self.difficulties:
            difficulties_item = difficulties_item_data.to_dict()
            difficulties.append(difficulties_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "requestId": request_id,
                "requestDescription": request_description,
                "leaderboardInfo": leaderboard_info,
                "created_at": created_at,
                "rankVotes": rank_votes,
                "qatVotes": qat_votes,
                "rankComments": rank_comments,
                "qatComments": qat_comments,
                "requestType": request_type,
                "approved": approved,
                "difficulties": difficulties,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.comment import Comment
        from ..models.leaderboard_info import LeaderboardInfo
        from ..models.ranking_difficulty import RankingDifficulty
        from ..models.vote_group import VoteGroup

        d = src_dict.copy()
        request_id = d.pop("requestId")

        request_description = d.pop("requestDescription")

        leaderboard_info = LeaderboardInfo.from_dict(d.pop("leaderboardInfo"))

        created_at = d.pop("created_at")

        rank_votes = VoteGroup.from_dict(d.pop("rankVotes"))

        qat_votes = VoteGroup.from_dict(d.pop("qatVotes"))

        rank_comments = []
        _rank_comments = d.pop("rankComments")
        for rank_comments_item_data in _rank_comments:
            rank_comments_item = Comment.from_dict(rank_comments_item_data)

            rank_comments.append(rank_comments_item)

        qat_comments = []
        _qat_comments = d.pop("qatComments")
        for qat_comments_item_data in _qat_comments:
            qat_comments_item = Comment.from_dict(qat_comments_item_data)

            qat_comments.append(qat_comments_item)

        request_type = d.pop("requestType")

        approved = d.pop("approved")

        difficulties = []
        _difficulties = d.pop("difficulties")
        for difficulties_item_data in _difficulties:
            difficulties_item = RankingDifficulty.from_dict(difficulties_item_data)

            difficulties.append(difficulties_item)

        rank_request_information = cls(
            request_id=request_id,
            request_description=request_description,
            leaderboard_info=leaderboard_info,
            created_at=created_at,
            rank_votes=rank_votes,
            qat_votes=qat_votes,
            rank_comments=rank_comments,
            qat_comments=qat_comments,
            request_type=request_type,
            approved=approved,
            difficulties=difficulties,
        )

        return rank_request_information
