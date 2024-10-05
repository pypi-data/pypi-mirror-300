from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="RankingDifficulty")


@_attrs_define
class RankingDifficulty:
    """
    Attributes:
        request_id (float):
        difficulty (float):
    """

    request_id: float
    difficulty: float

    def to_dict(self) -> Dict[str, Any]:
        request_id = self.request_id

        difficulty = self.difficulty

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "requestId": request_id,
                "difficulty": difficulty,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_id = d.pop("requestId")

        difficulty = d.pop("difficulty")

        ranking_difficulty = cls(
            request_id=request_id,
            difficulty=difficulty,
        )

        return ranking_difficulty
