from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.map_stats_sentiment import MapStatsSentiment
from ..types import UNSET, Unset

T = TypeVar("T", bound="MapStats")


@_attrs_define
class MapStats:
    """
    Attributes:
        downloads (Union[Unset, int]):
        downvotes (Union[Unset, int]):
        plays (Union[Unset, int]):
        reviews (Union[Unset, int]):
        score (Union[Unset, Any]):
        score_one_dp (Union[Unset, Any]):
        sentiment (Union[Unset, MapStatsSentiment]):
        upvotes (Union[Unset, int]):
    """

    downloads: Union[Unset, int] = UNSET
    downvotes: Union[Unset, int] = UNSET
    plays: Union[Unset, int] = UNSET
    reviews: Union[Unset, int] = UNSET
    score: Union[Unset, Any] = UNSET
    score_one_dp: Union[Unset, Any] = UNSET
    sentiment: Union[Unset, MapStatsSentiment] = UNSET
    upvotes: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        downloads = self.downloads

        downvotes = self.downvotes

        plays = self.plays

        reviews = self.reviews

        score = self.score

        score_one_dp = self.score_one_dp

        sentiment: Union[Unset, str] = UNSET
        if not isinstance(self.sentiment, Unset):
            sentiment = self.sentiment.value

        upvotes = self.upvotes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if downloads is not UNSET:
            field_dict["downloads"] = downloads
        if downvotes is not UNSET:
            field_dict["downvotes"] = downvotes
        if plays is not UNSET:
            field_dict["plays"] = plays
        if reviews is not UNSET:
            field_dict["reviews"] = reviews
        if score is not UNSET:
            field_dict["score"] = score
        if score_one_dp is not UNSET:
            field_dict["scoreOneDP"] = score_one_dp
        if sentiment is not UNSET:
            field_dict["sentiment"] = sentiment
        if upvotes is not UNSET:
            field_dict["upvotes"] = upvotes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        downloads = d.pop("downloads", UNSET)

        downvotes = d.pop("downvotes", UNSET)

        plays = d.pop("plays", UNSET)

        reviews = d.pop("reviews", UNSET)

        score = d.pop("score", UNSET)

        score_one_dp = d.pop("scoreOneDP", UNSET)

        _sentiment = d.pop("sentiment", UNSET)
        sentiment: Union[Unset, MapStatsSentiment]
        if isinstance(_sentiment, Unset):
            sentiment = UNSET
        else:
            sentiment = MapStatsSentiment(_sentiment)

        upvotes = d.pop("upvotes", UNSET)

        map_stats = cls(
            downloads=downloads,
            downvotes=downvotes,
            plays=plays,
            reviews=reviews,
            score=score,
            score_one_dp=score_one_dp,
            sentiment=sentiment,
            upvotes=upvotes,
        )

        map_stats.additional_properties = d
        return map_stats

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
