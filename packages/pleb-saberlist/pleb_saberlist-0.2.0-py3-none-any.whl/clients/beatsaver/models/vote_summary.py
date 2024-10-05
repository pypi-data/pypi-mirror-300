from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VoteSummary")


@_attrs_define
class VoteSummary:
    """
    Attributes:
        downvotes (Union[Unset, int]):
        hash_ (Union[Unset, str]):
        key64 (Union[Unset, str]):
        map_id (Union[Unset, int]):
        score (Union[Unset, float]):
        upvotes (Union[Unset, int]):
    """

    downvotes: Union[Unset, int] = UNSET
    hash_: Union[Unset, str] = UNSET
    key64: Union[Unset, str] = UNSET
    map_id: Union[Unset, int] = UNSET
    score: Union[Unset, float] = UNSET
    upvotes: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        downvotes = self.downvotes

        hash_ = self.hash_

        key64 = self.key64

        map_id = self.map_id

        score = self.score

        upvotes = self.upvotes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if downvotes is not UNSET:
            field_dict["downvotes"] = downvotes
        if hash_ is not UNSET:
            field_dict["hash"] = hash_
        if key64 is not UNSET:
            field_dict["key64"] = key64
        if map_id is not UNSET:
            field_dict["mapId"] = map_id
        if score is not UNSET:
            field_dict["score"] = score
        if upvotes is not UNSET:
            field_dict["upvotes"] = upvotes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        downvotes = d.pop("downvotes", UNSET)

        hash_ = d.pop("hash", UNSET)

        key64 = d.pop("key64", UNSET)

        map_id = d.pop("mapId", UNSET)

        score = d.pop("score", UNSET)

        upvotes = d.pop("upvotes", UNSET)

        vote_summary = cls(
            downvotes=downvotes,
            hash_=hash_,
            key64=key64,
            map_id=map_id,
            score=score,
            upvotes=upvotes,
        )

        vote_summary.additional_properties = d
        return vote_summary

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
