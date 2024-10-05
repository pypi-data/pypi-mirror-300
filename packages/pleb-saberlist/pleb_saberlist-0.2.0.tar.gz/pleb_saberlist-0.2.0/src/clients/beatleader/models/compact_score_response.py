from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.compact_leaderboard import CompactLeaderboard
    from ..models.compact_score import CompactScore


T = TypeVar("T", bound="CompactScoreResponse")


@_attrs_define
class CompactScoreResponse:
    """
    Attributes:
        score (Union[Unset, CompactScore]):
        leaderboard (Union[Unset, CompactLeaderboard]):
    """

    score: Union[Unset, "CompactScore"] = UNSET
    leaderboard: Union[Unset, "CompactLeaderboard"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        score: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.score, Unset):
            score = self.score.to_dict()

        leaderboard: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.leaderboard, Unset):
            leaderboard = self.leaderboard.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if score is not UNSET:
            field_dict["score"] = score
        if leaderboard is not UNSET:
            field_dict["leaderboard"] = leaderboard

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.compact_leaderboard import CompactLeaderboard
        from ..models.compact_score import CompactScore

        d = src_dict.copy()
        _score = d.pop("score", UNSET)
        score: Union[Unset, CompactScore]
        if isinstance(_score, Unset):
            score = UNSET
        else:
            score = CompactScore.from_dict(_score)

        _leaderboard = d.pop("leaderboard", UNSET)
        leaderboard: Union[Unset, CompactLeaderboard]
        if isinstance(_leaderboard, Unset):
            leaderboard = UNSET
        else:
            leaderboard = CompactLeaderboard.from_dict(_leaderboard)

        compact_score_response = cls(
            score=score,
            leaderboard=leaderboard,
        )

        return compact_score_response
