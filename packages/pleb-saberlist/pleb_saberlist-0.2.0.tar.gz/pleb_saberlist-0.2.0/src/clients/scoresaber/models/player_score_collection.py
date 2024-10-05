from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.player_score import PlayerScore


T = TypeVar("T", bound="PlayerScoreCollection")


@_attrs_define
class PlayerScoreCollection:
    """
    Attributes:
        player_scores (List['PlayerScore']):
        metadata (Metadata):
    """

    player_scores: List["PlayerScore"]
    metadata: "Metadata"

    def to_dict(self) -> Dict[str, Any]:
        player_scores = []
        for player_scores_item_data in self.player_scores:
            player_scores_item = player_scores_item_data.to_dict()
            player_scores.append(player_scores_item)

        metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "playerScores": player_scores,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metadata import Metadata
        from ..models.player_score import PlayerScore

        d = src_dict.copy()
        player_scores = []
        _player_scores = d.pop("playerScores")
        for player_scores_item_data in _player_scores:
            player_scores_item = PlayerScore.from_dict(player_scores_item_data)

            player_scores.append(player_scores_item)

        metadata = Metadata.from_dict(d.pop("metadata"))

        player_score_collection = cls(
            player_scores=player_scores,
            metadata=metadata,
        )

        return player_score_collection
