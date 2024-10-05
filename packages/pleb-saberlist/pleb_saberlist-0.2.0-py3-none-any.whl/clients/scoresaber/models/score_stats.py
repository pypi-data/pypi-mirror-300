from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ScoreStats")


@_attrs_define
class ScoreStats:
    """
    Attributes:
        total_score (float):
        total_ranked_score (float):
        average_ranked_accuracy (float):
        total_play_count (float):
        ranked_play_count (float):
        replays_watched (float):
    """

    total_score: float
    total_ranked_score: float
    average_ranked_accuracy: float
    total_play_count: float
    ranked_play_count: float
    replays_watched: float

    def to_dict(self) -> Dict[str, Any]:
        total_score = self.total_score

        total_ranked_score = self.total_ranked_score

        average_ranked_accuracy = self.average_ranked_accuracy

        total_play_count = self.total_play_count

        ranked_play_count = self.ranked_play_count

        replays_watched = self.replays_watched

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "totalScore": total_score,
                "totalRankedScore": total_ranked_score,
                "averageRankedAccuracy": average_ranked_accuracy,
                "totalPlayCount": total_play_count,
                "rankedPlayCount": ranked_play_count,
                "replaysWatched": replays_watched,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_score = d.pop("totalScore")

        total_ranked_score = d.pop("totalRankedScore")

        average_ranked_accuracy = d.pop("averageRankedAccuracy")

        total_play_count = d.pop("totalPlayCount")

        ranked_play_count = d.pop("rankedPlayCount")

        replays_watched = d.pop("replaysWatched")

        score_stats = cls(
            total_score=total_score,
            total_ranked_score=total_ranked_score,
            average_ranked_accuracy=average_ranked_accuracy,
            total_play_count=total_play_count,
            ranked_play_count=ranked_play_count,
            replays_watched=replays_watched,
        )

        return score_stats
