from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.clan_response_full import ClanResponseFull
    from ..models.leaderboard_response import LeaderboardResponse
    from ..models.score_response import ScoreResponse
    from ..models.score_response_with_acc import ScoreResponseWithAcc


T = TypeVar("T", bound="ClanRankingResponse")


@_attrs_define
class ClanRankingResponse:
    """
    Attributes:
        id (Union[Unset, int]):
        clan (Union[Unset, ClanResponseFull]):
        last_update_time (Union[Unset, int]):
        average_rank (Union[Unset, float]):
        rank (Union[Unset, int]):
        pp (Union[Unset, float]):
        average_accuracy (Union[Unset, float]):
        total_score (Union[Unset, float]):
        leaderboard_id (Union[None, Unset, str]):
        leaderboard (Union[Unset, LeaderboardResponse]):
        associated_scores (Union[List['ScoreResponse'], None, Unset]):
        associated_scores_count (Union[Unset, int]):
        my_score (Union[Unset, ScoreResponseWithAcc]):
    """

    id: Union[Unset, int] = UNSET
    clan: Union[Unset, "ClanResponseFull"] = UNSET
    last_update_time: Union[Unset, int] = UNSET
    average_rank: Union[Unset, float] = UNSET
    rank: Union[Unset, int] = UNSET
    pp: Union[Unset, float] = UNSET
    average_accuracy: Union[Unset, float] = UNSET
    total_score: Union[Unset, float] = UNSET
    leaderboard_id: Union[None, Unset, str] = UNSET
    leaderboard: Union[Unset, "LeaderboardResponse"] = UNSET
    associated_scores: Union[List["ScoreResponse"], None, Unset] = UNSET
    associated_scores_count: Union[Unset, int] = UNSET
    my_score: Union[Unset, "ScoreResponseWithAcc"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        clan: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.clan, Unset):
            clan = self.clan.to_dict()

        last_update_time = self.last_update_time

        average_rank = self.average_rank

        rank = self.rank

        pp = self.pp

        average_accuracy = self.average_accuracy

        total_score = self.total_score

        leaderboard_id: Union[None, Unset, str]
        if isinstance(self.leaderboard_id, Unset):
            leaderboard_id = UNSET
        else:
            leaderboard_id = self.leaderboard_id

        leaderboard: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.leaderboard, Unset):
            leaderboard = self.leaderboard.to_dict()

        associated_scores: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.associated_scores, Unset):
            associated_scores = UNSET
        elif isinstance(self.associated_scores, list):
            associated_scores = []
            for associated_scores_type_0_item_data in self.associated_scores:
                associated_scores_type_0_item = associated_scores_type_0_item_data.to_dict()
                associated_scores.append(associated_scores_type_0_item)

        else:
            associated_scores = self.associated_scores

        associated_scores_count = self.associated_scores_count

        my_score: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.my_score, Unset):
            my_score = self.my_score.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if clan is not UNSET:
            field_dict["clan"] = clan
        if last_update_time is not UNSET:
            field_dict["lastUpdateTime"] = last_update_time
        if average_rank is not UNSET:
            field_dict["averageRank"] = average_rank
        if rank is not UNSET:
            field_dict["rank"] = rank
        if pp is not UNSET:
            field_dict["pp"] = pp
        if average_accuracy is not UNSET:
            field_dict["averageAccuracy"] = average_accuracy
        if total_score is not UNSET:
            field_dict["totalScore"] = total_score
        if leaderboard_id is not UNSET:
            field_dict["leaderboardId"] = leaderboard_id
        if leaderboard is not UNSET:
            field_dict["leaderboard"] = leaderboard
        if associated_scores is not UNSET:
            field_dict["associatedScores"] = associated_scores
        if associated_scores_count is not UNSET:
            field_dict["associatedScoresCount"] = associated_scores_count
        if my_score is not UNSET:
            field_dict["myScore"] = my_score

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.clan_response_full import ClanResponseFull
        from ..models.leaderboard_response import LeaderboardResponse
        from ..models.score_response import ScoreResponse
        from ..models.score_response_with_acc import ScoreResponseWithAcc

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _clan = d.pop("clan", UNSET)
        clan: Union[Unset, ClanResponseFull]
        if isinstance(_clan, Unset):
            clan = UNSET
        else:
            clan = ClanResponseFull.from_dict(_clan)

        last_update_time = d.pop("lastUpdateTime", UNSET)

        average_rank = d.pop("averageRank", UNSET)

        rank = d.pop("rank", UNSET)

        pp = d.pop("pp", UNSET)

        average_accuracy = d.pop("averageAccuracy", UNSET)

        total_score = d.pop("totalScore", UNSET)

        def _parse_leaderboard_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        leaderboard_id = _parse_leaderboard_id(d.pop("leaderboardId", UNSET))

        _leaderboard = d.pop("leaderboard", UNSET)
        leaderboard: Union[Unset, LeaderboardResponse]
        if isinstance(_leaderboard, Unset):
            leaderboard = UNSET
        else:
            leaderboard = LeaderboardResponse.from_dict(_leaderboard)

        def _parse_associated_scores(data: object) -> Union[List["ScoreResponse"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                associated_scores_type_0 = []
                _associated_scores_type_0 = data
                for associated_scores_type_0_item_data in _associated_scores_type_0:
                    associated_scores_type_0_item = ScoreResponse.from_dict(associated_scores_type_0_item_data)

                    associated_scores_type_0.append(associated_scores_type_0_item)

                return associated_scores_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ScoreResponse"], None, Unset], data)

        associated_scores = _parse_associated_scores(d.pop("associatedScores", UNSET))

        associated_scores_count = d.pop("associatedScoresCount", UNSET)

        _my_score = d.pop("myScore", UNSET)
        my_score: Union[Unset, ScoreResponseWithAcc]
        if isinstance(_my_score, Unset):
            my_score = UNSET
        else:
            my_score = ScoreResponseWithAcc.from_dict(_my_score)

        clan_ranking_response = cls(
            id=id,
            clan=clan,
            last_update_time=last_update_time,
            average_rank=average_rank,
            rank=rank,
            pp=pp,
            average_accuracy=average_accuracy,
            total_score=total_score,
            leaderboard_id=leaderboard_id,
            leaderboard=leaderboard,
            associated_scores=associated_scores,
            associated_scores_count=associated_scores_count,
            my_score=my_score,
        )

        return clan_ranking_response
