from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.leaderboard_info import LeaderboardInfo
    from ..models.score import Score


T = TypeVar("T", bound="PlayerScore")


@_attrs_define
class PlayerScore:
    """
    Attributes:
        score (Score):
        leaderboard (LeaderboardInfo):
    """

    score: "Score"
    leaderboard: "LeaderboardInfo"

    def to_dict(self) -> Dict[str, Any]:
        score = self.score.to_dict()

        leaderboard = self.leaderboard.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "score": score,
                "leaderboard": leaderboard,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.leaderboard_info import LeaderboardInfo
        from ..models.score import Score

        d = src_dict.copy()
        score = Score.from_dict(d.pop("score"))

        leaderboard = LeaderboardInfo.from_dict(d.pop("leaderboard"))

        player_score = cls(
            score=score,
            leaderboard=leaderboard,
        )

        return player_score
