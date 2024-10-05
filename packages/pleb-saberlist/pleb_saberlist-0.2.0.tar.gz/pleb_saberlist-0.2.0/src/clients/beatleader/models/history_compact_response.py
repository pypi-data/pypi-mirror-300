from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="HistoryCompactResponse")


@_attrs_define
class HistoryCompactResponse:
    """
    Attributes:
        timestamp (Union[Unset, int]):
        pp (Union[Unset, float]):
        rank (Union[Unset, int]):
        country_rank (Union[Unset, int]):
        average_ranked_accuracy (Union[Unset, float]):
        average_unranked_accuracy (Union[Unset, float]):
        average_accuracy (Union[Unset, float]):
        median_ranked_accuracy (Union[Unset, float]):
        median_accuracy (Union[Unset, float]):
        ranked_play_count (Union[Unset, int]):
        unranked_play_count (Union[Unset, int]):
        total_play_count (Union[Unset, int]):
        ranked_improvements_count (Union[Unset, int]):
        unranked_improvements_count (Union[Unset, int]):
        total_improvements_count (Union[Unset, int]):
    """

    timestamp: Union[Unset, int] = UNSET
    pp: Union[Unset, float] = UNSET
    rank: Union[Unset, int] = UNSET
    country_rank: Union[Unset, int] = UNSET
    average_ranked_accuracy: Union[Unset, float] = UNSET
    average_unranked_accuracy: Union[Unset, float] = UNSET
    average_accuracy: Union[Unset, float] = UNSET
    median_ranked_accuracy: Union[Unset, float] = UNSET
    median_accuracy: Union[Unset, float] = UNSET
    ranked_play_count: Union[Unset, int] = UNSET
    unranked_play_count: Union[Unset, int] = UNSET
    total_play_count: Union[Unset, int] = UNSET
    ranked_improvements_count: Union[Unset, int] = UNSET
    unranked_improvements_count: Union[Unset, int] = UNSET
    total_improvements_count: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        timestamp = self.timestamp

        pp = self.pp

        rank = self.rank

        country_rank = self.country_rank

        average_ranked_accuracy = self.average_ranked_accuracy

        average_unranked_accuracy = self.average_unranked_accuracy

        average_accuracy = self.average_accuracy

        median_ranked_accuracy = self.median_ranked_accuracy

        median_accuracy = self.median_accuracy

        ranked_play_count = self.ranked_play_count

        unranked_play_count = self.unranked_play_count

        total_play_count = self.total_play_count

        ranked_improvements_count = self.ranked_improvements_count

        unranked_improvements_count = self.unranked_improvements_count

        total_improvements_count = self.total_improvements_count

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if pp is not UNSET:
            field_dict["pp"] = pp
        if rank is not UNSET:
            field_dict["rank"] = rank
        if country_rank is not UNSET:
            field_dict["countryRank"] = country_rank
        if average_ranked_accuracy is not UNSET:
            field_dict["averageRankedAccuracy"] = average_ranked_accuracy
        if average_unranked_accuracy is not UNSET:
            field_dict["averageUnrankedAccuracy"] = average_unranked_accuracy
        if average_accuracy is not UNSET:
            field_dict["averageAccuracy"] = average_accuracy
        if median_ranked_accuracy is not UNSET:
            field_dict["medianRankedAccuracy"] = median_ranked_accuracy
        if median_accuracy is not UNSET:
            field_dict["medianAccuracy"] = median_accuracy
        if ranked_play_count is not UNSET:
            field_dict["rankedPlayCount"] = ranked_play_count
        if unranked_play_count is not UNSET:
            field_dict["unrankedPlayCount"] = unranked_play_count
        if total_play_count is not UNSET:
            field_dict["totalPlayCount"] = total_play_count
        if ranked_improvements_count is not UNSET:
            field_dict["rankedImprovementsCount"] = ranked_improvements_count
        if unranked_improvements_count is not UNSET:
            field_dict["unrankedImprovementsCount"] = unranked_improvements_count
        if total_improvements_count is not UNSET:
            field_dict["totalImprovementsCount"] = total_improvements_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        timestamp = d.pop("timestamp", UNSET)

        pp = d.pop("pp", UNSET)

        rank = d.pop("rank", UNSET)

        country_rank = d.pop("countryRank", UNSET)

        average_ranked_accuracy = d.pop("averageRankedAccuracy", UNSET)

        average_unranked_accuracy = d.pop("averageUnrankedAccuracy", UNSET)

        average_accuracy = d.pop("averageAccuracy", UNSET)

        median_ranked_accuracy = d.pop("medianRankedAccuracy", UNSET)

        median_accuracy = d.pop("medianAccuracy", UNSET)

        ranked_play_count = d.pop("rankedPlayCount", UNSET)

        unranked_play_count = d.pop("unrankedPlayCount", UNSET)

        total_play_count = d.pop("totalPlayCount", UNSET)

        ranked_improvements_count = d.pop("rankedImprovementsCount", UNSET)

        unranked_improvements_count = d.pop("unrankedImprovementsCount", UNSET)

        total_improvements_count = d.pop("totalImprovementsCount", UNSET)

        history_compact_response = cls(
            timestamp=timestamp,
            pp=pp,
            rank=rank,
            country_rank=country_rank,
            average_ranked_accuracy=average_ranked_accuracy,
            average_unranked_accuracy=average_unranked_accuracy,
            average_accuracy=average_accuracy,
            median_ranked_accuracy=median_ranked_accuracy,
            median_accuracy=median_accuracy,
            ranked_play_count=ranked_play_count,
            unranked_play_count=unranked_play_count,
            total_play_count=total_play_count,
            ranked_improvements_count=ranked_improvements_count,
            unranked_improvements_count=unranked_improvements_count,
            total_improvements_count=total_improvements_count,
        )

        return history_compact_response
