from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.score import Score


T = TypeVar("T", bound="ScoreCollection")


@_attrs_define
class ScoreCollection:
    """
    Attributes:
        scores (List['Score']):
        metadata (Metadata):
    """

    scores: List["Score"]
    metadata: "Metadata"

    def to_dict(self) -> Dict[str, Any]:
        scores = []
        for scores_item_data in self.scores:
            scores_item = scores_item_data.to_dict()
            scores.append(scores_item)

        metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "scores": scores,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metadata import Metadata
        from ..models.score import Score

        d = src_dict.copy()
        scores = []
        _scores = d.pop("scores")
        for scores_item_data in _scores:
            scores_item = Score.from_dict(scores_item_data)

            scores.append(scores_item)

        metadata = Metadata.from_dict(d.pop("metadata"))

        score_collection = cls(
            scores=scores,
            metadata=metadata,
        )

        return score_collection
