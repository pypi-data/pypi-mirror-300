import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_diff_stats import UserDiffStats


T = TypeVar("T", bound="UserStats")


@_attrs_define
class UserStats:
    """
    Attributes:
        avg_bpm (Union[Unset, Any]):
        avg_duration (Union[Unset, Any]):
        avg_score (Union[Unset, Any]):
        diff_stats (Union[Unset, UserDiffStats]):
        first_upload (Union[Unset, datetime.datetime]):
        last_upload (Union[Unset, datetime.datetime]):
        ranked_maps (Union[Unset, int]):
        total_downvotes (Union[Unset, int]):
        total_maps (Union[Unset, int]):
        total_upvotes (Union[Unset, int]):
    """

    avg_bpm: Union[Unset, Any] = UNSET
    avg_duration: Union[Unset, Any] = UNSET
    avg_score: Union[Unset, Any] = UNSET
    diff_stats: Union[Unset, "UserDiffStats"] = UNSET
    first_upload: Union[Unset, datetime.datetime] = UNSET
    last_upload: Union[Unset, datetime.datetime] = UNSET
    ranked_maps: Union[Unset, int] = UNSET
    total_downvotes: Union[Unset, int] = UNSET
    total_maps: Union[Unset, int] = UNSET
    total_upvotes: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        avg_bpm = self.avg_bpm

        avg_duration = self.avg_duration

        avg_score = self.avg_score

        diff_stats: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.diff_stats, Unset):
            diff_stats = self.diff_stats.to_dict()

        first_upload: Union[Unset, str] = UNSET
        if not isinstance(self.first_upload, Unset):
            first_upload = self.first_upload.isoformat()

        last_upload: Union[Unset, str] = UNSET
        if not isinstance(self.last_upload, Unset):
            last_upload = self.last_upload.isoformat()

        ranked_maps = self.ranked_maps

        total_downvotes = self.total_downvotes

        total_maps = self.total_maps

        total_upvotes = self.total_upvotes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avg_bpm is not UNSET:
            field_dict["avgBpm"] = avg_bpm
        if avg_duration is not UNSET:
            field_dict["avgDuration"] = avg_duration
        if avg_score is not UNSET:
            field_dict["avgScore"] = avg_score
        if diff_stats is not UNSET:
            field_dict["diffStats"] = diff_stats
        if first_upload is not UNSET:
            field_dict["firstUpload"] = first_upload
        if last_upload is not UNSET:
            field_dict["lastUpload"] = last_upload
        if ranked_maps is not UNSET:
            field_dict["rankedMaps"] = ranked_maps
        if total_downvotes is not UNSET:
            field_dict["totalDownvotes"] = total_downvotes
        if total_maps is not UNSET:
            field_dict["totalMaps"] = total_maps
        if total_upvotes is not UNSET:
            field_dict["totalUpvotes"] = total_upvotes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_diff_stats import UserDiffStats

        d = src_dict.copy()
        avg_bpm = d.pop("avgBpm", UNSET)

        avg_duration = d.pop("avgDuration", UNSET)

        avg_score = d.pop("avgScore", UNSET)

        _diff_stats = d.pop("diffStats", UNSET)
        diff_stats: Union[Unset, UserDiffStats]
        if isinstance(_diff_stats, Unset):
            diff_stats = UNSET
        else:
            diff_stats = UserDiffStats.from_dict(_diff_stats)

        _first_upload = d.pop("firstUpload", UNSET)
        first_upload: Union[Unset, datetime.datetime]
        if isinstance(_first_upload, Unset):
            first_upload = UNSET
        else:
            first_upload = isoparse(_first_upload)

        _last_upload = d.pop("lastUpload", UNSET)
        last_upload: Union[Unset, datetime.datetime]
        if isinstance(_last_upload, Unset):
            last_upload = UNSET
        else:
            last_upload = isoparse(_last_upload)

        ranked_maps = d.pop("rankedMaps", UNSET)

        total_downvotes = d.pop("totalDownvotes", UNSET)

        total_maps = d.pop("totalMaps", UNSET)

        total_upvotes = d.pop("totalUpvotes", UNSET)

        user_stats = cls(
            avg_bpm=avg_bpm,
            avg_duration=avg_duration,
            avg_score=avg_score,
            diff_stats=diff_stats,
            first_upload=first_upload,
            last_upload=last_upload,
            ranked_maps=ranked_maps,
            total_downvotes=total_downvotes,
            total_maps=total_maps,
            total_upvotes=total_upvotes,
        )

        user_stats.additional_properties = d
        return user_stats

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
