from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScoreImprovement")


@_attrs_define
class ScoreImprovement:
    """
    Attributes:
        id (Union[Unset, int]):
        timeset (Union[None, Unset, str]):
        score (Union[Unset, int]):
        accuracy (Union[Unset, float]):
        pp (Union[Unset, float]):
        bonus_pp (Union[Unset, float]):
        rank (Union[Unset, int]):
        acc_right (Union[Unset, float]):
        acc_left (Union[Unset, float]):
        average_ranked_accuracy (Union[Unset, float]):
        total_pp (Union[Unset, float]):
        total_rank (Union[Unset, int]):
        bad_cuts (Union[Unset, int]):
        missed_notes (Union[Unset, int]):
        bomb_cuts (Union[Unset, int]):
        walls_hit (Union[Unset, int]):
        pauses (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    timeset: Union[None, Unset, str] = UNSET
    score: Union[Unset, int] = UNSET
    accuracy: Union[Unset, float] = UNSET
    pp: Union[Unset, float] = UNSET
    bonus_pp: Union[Unset, float] = UNSET
    rank: Union[Unset, int] = UNSET
    acc_right: Union[Unset, float] = UNSET
    acc_left: Union[Unset, float] = UNSET
    average_ranked_accuracy: Union[Unset, float] = UNSET
    total_pp: Union[Unset, float] = UNSET
    total_rank: Union[Unset, int] = UNSET
    bad_cuts: Union[Unset, int] = UNSET
    missed_notes: Union[Unset, int] = UNSET
    bomb_cuts: Union[Unset, int] = UNSET
    walls_hit: Union[Unset, int] = UNSET
    pauses: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        timeset: Union[None, Unset, str]
        if isinstance(self.timeset, Unset):
            timeset = UNSET
        else:
            timeset = self.timeset

        score = self.score

        accuracy = self.accuracy

        pp = self.pp

        bonus_pp = self.bonus_pp

        rank = self.rank

        acc_right = self.acc_right

        acc_left = self.acc_left

        average_ranked_accuracy = self.average_ranked_accuracy

        total_pp = self.total_pp

        total_rank = self.total_rank

        bad_cuts = self.bad_cuts

        missed_notes = self.missed_notes

        bomb_cuts = self.bomb_cuts

        walls_hit = self.walls_hit

        pauses = self.pauses

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if timeset is not UNSET:
            field_dict["timeset"] = timeset
        if score is not UNSET:
            field_dict["score"] = score
        if accuracy is not UNSET:
            field_dict["accuracy"] = accuracy
        if pp is not UNSET:
            field_dict["pp"] = pp
        if bonus_pp is not UNSET:
            field_dict["bonusPp"] = bonus_pp
        if rank is not UNSET:
            field_dict["rank"] = rank
        if acc_right is not UNSET:
            field_dict["accRight"] = acc_right
        if acc_left is not UNSET:
            field_dict["accLeft"] = acc_left
        if average_ranked_accuracy is not UNSET:
            field_dict["averageRankedAccuracy"] = average_ranked_accuracy
        if total_pp is not UNSET:
            field_dict["totalPp"] = total_pp
        if total_rank is not UNSET:
            field_dict["totalRank"] = total_rank
        if bad_cuts is not UNSET:
            field_dict["badCuts"] = bad_cuts
        if missed_notes is not UNSET:
            field_dict["missedNotes"] = missed_notes
        if bomb_cuts is not UNSET:
            field_dict["bombCuts"] = bomb_cuts
        if walls_hit is not UNSET:
            field_dict["wallsHit"] = walls_hit
        if pauses is not UNSET:
            field_dict["pauses"] = pauses

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_timeset(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        timeset = _parse_timeset(d.pop("timeset", UNSET))

        score = d.pop("score", UNSET)

        accuracy = d.pop("accuracy", UNSET)

        pp = d.pop("pp", UNSET)

        bonus_pp = d.pop("bonusPp", UNSET)

        rank = d.pop("rank", UNSET)

        acc_right = d.pop("accRight", UNSET)

        acc_left = d.pop("accLeft", UNSET)

        average_ranked_accuracy = d.pop("averageRankedAccuracy", UNSET)

        total_pp = d.pop("totalPp", UNSET)

        total_rank = d.pop("totalRank", UNSET)

        bad_cuts = d.pop("badCuts", UNSET)

        missed_notes = d.pop("missedNotes", UNSET)

        bomb_cuts = d.pop("bombCuts", UNSET)

        walls_hit = d.pop("wallsHit", UNSET)

        pauses = d.pop("pauses", UNSET)

        score_improvement = cls(
            id=id,
            timeset=timeset,
            score=score,
            accuracy=accuracy,
            pp=pp,
            bonus_pp=bonus_pp,
            rank=rank,
            acc_right=acc_right,
            acc_left=acc_left,
            average_ranked_accuracy=average_ranked_accuracy,
            total_pp=total_pp,
            total_rank=total_rank,
            bad_cuts=bad_cuts,
            missed_notes=missed_notes,
            bomb_cuts=bomb_cuts,
            walls_hit=walls_hit,
            pauses=pauses,
        )

        return score_improvement
