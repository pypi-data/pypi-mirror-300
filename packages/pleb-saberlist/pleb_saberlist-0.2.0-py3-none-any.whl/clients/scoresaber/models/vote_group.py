from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="VoteGroup")


@_attrs_define
class VoteGroup:
    """
    Attributes:
        upvotes (float):
        downvotes (float):
        my_vote (bool):
        neutral (Union[Unset, float]):
    """

    upvotes: float
    downvotes: float
    my_vote: bool
    neutral: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        upvotes = self.upvotes

        downvotes = self.downvotes

        my_vote = self.my_vote

        neutral = self.neutral

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "upvotes": upvotes,
                "downvotes": downvotes,
                "myVote": my_vote,
            }
        )
        if neutral is not UNSET:
            field_dict["neutral"] = neutral

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        upvotes = d.pop("upvotes")

        downvotes = d.pop("downvotes")

        my_vote = d.pop("myVote")

        neutral = d.pop("neutral", UNSET)

        vote_group = cls(
            upvotes=upvotes,
            downvotes=downvotes,
            my_vote=my_vote,
            neutral=neutral,
        )

        return vote_group
