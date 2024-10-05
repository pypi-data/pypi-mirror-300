from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlaylistStats")


@_attrs_define
class PlaylistStats:
    """
    Attributes:
        avg_score (Union[Unset, Any]):
        down_votes (Union[Unset, int]):
        mapper_count (Union[Unset, int]):
        max_nps (Union[Unset, float]):
        max_nps_two_dp (Union[Unset, float]):
        min_nps (Union[Unset, float]):
        min_nps_two_dp (Union[Unset, float]):
        score_one_dp (Union[Unset, Any]):
        total_duration (Union[Unset, int]):
        total_maps (Union[Unset, int]):
        up_votes (Union[Unset, int]):
    """

    avg_score: Union[Unset, Any] = UNSET
    down_votes: Union[Unset, int] = UNSET
    mapper_count: Union[Unset, int] = UNSET
    max_nps: Union[Unset, float] = UNSET
    max_nps_two_dp: Union[Unset, float] = UNSET
    min_nps: Union[Unset, float] = UNSET
    min_nps_two_dp: Union[Unset, float] = UNSET
    score_one_dp: Union[Unset, Any] = UNSET
    total_duration: Union[Unset, int] = UNSET
    total_maps: Union[Unset, int] = UNSET
    up_votes: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        avg_score = self.avg_score

        down_votes = self.down_votes

        mapper_count = self.mapper_count

        max_nps = self.max_nps

        max_nps_two_dp = self.max_nps_two_dp

        min_nps = self.min_nps

        min_nps_two_dp = self.min_nps_two_dp

        score_one_dp = self.score_one_dp

        total_duration = self.total_duration

        total_maps = self.total_maps

        up_votes = self.up_votes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avg_score is not UNSET:
            field_dict["avgScore"] = avg_score
        if down_votes is not UNSET:
            field_dict["downVotes"] = down_votes
        if mapper_count is not UNSET:
            field_dict["mapperCount"] = mapper_count
        if max_nps is not UNSET:
            field_dict["maxNps"] = max_nps
        if max_nps_two_dp is not UNSET:
            field_dict["maxNpsTwoDP"] = max_nps_two_dp
        if min_nps is not UNSET:
            field_dict["minNps"] = min_nps
        if min_nps_two_dp is not UNSET:
            field_dict["minNpsTwoDP"] = min_nps_two_dp
        if score_one_dp is not UNSET:
            field_dict["scoreOneDP"] = score_one_dp
        if total_duration is not UNSET:
            field_dict["totalDuration"] = total_duration
        if total_maps is not UNSET:
            field_dict["totalMaps"] = total_maps
        if up_votes is not UNSET:
            field_dict["upVotes"] = up_votes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        avg_score = d.pop("avgScore", UNSET)

        down_votes = d.pop("downVotes", UNSET)

        mapper_count = d.pop("mapperCount", UNSET)

        max_nps = d.pop("maxNps", UNSET)

        max_nps_two_dp = d.pop("maxNpsTwoDP", UNSET)

        min_nps = d.pop("minNps", UNSET)

        min_nps_two_dp = d.pop("minNpsTwoDP", UNSET)

        score_one_dp = d.pop("scoreOneDP", UNSET)

        total_duration = d.pop("totalDuration", UNSET)

        total_maps = d.pop("totalMaps", UNSET)

        up_votes = d.pop("upVotes", UNSET)

        playlist_stats = cls(
            avg_score=avg_score,
            down_votes=down_votes,
            mapper_count=mapper_count,
            max_nps=max_nps,
            max_nps_two_dp=max_nps_two_dp,
            min_nps=min_nps,
            min_nps_two_dp=min_nps_two_dp,
            score_one_dp=score_one_dp,
            total_duration=total_duration,
            total_maps=total_maps,
            up_votes=up_votes,
        )

        playlist_stats.additional_properties = d
        return playlist_stats

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
