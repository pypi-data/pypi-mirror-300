from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="Difficulty")


@_attrs_define
class Difficulty:
    """
    Attributes:
        leaderboard_id (float):
        difficulty (float):
        game_mode (str):
        difficulty_raw (str):
    """

    leaderboard_id: float
    difficulty: float
    game_mode: str
    difficulty_raw: str

    def to_dict(self) -> Dict[str, Any]:
        leaderboard_id = self.leaderboard_id

        difficulty = self.difficulty

        game_mode = self.game_mode

        difficulty_raw = self.difficulty_raw

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "leaderboardId": leaderboard_id,
                "difficulty": difficulty,
                "gameMode": game_mode,
                "difficultyRaw": difficulty_raw,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        leaderboard_id = d.pop("leaderboardId")

        difficulty = d.pop("difficulty")

        game_mode = d.pop("gameMode")

        difficulty_raw = d.pop("difficultyRaw")

        difficulty = cls(
            leaderboard_id=leaderboard_id,
            difficulty=difficulty,
            game_mode=game_mode,
            difficulty_raw=difficulty_raw,
        )

        return difficulty
