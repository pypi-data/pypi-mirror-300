from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.compact_song_response import CompactSongResponse
    from ..models.difficulty_response import DifficultyResponse


T = TypeVar("T", bound="CompactLeaderboardResponse")


@_attrs_define
class CompactLeaderboardResponse:
    """
    Attributes:
        id (Union[None, Unset, str]):
        song (Union[Unset, CompactSongResponse]):
        difficulty (Union[Unset, DifficultyResponse]):
    """

    id: Union[None, Unset, str] = UNSET
    song: Union[Unset, "CompactSongResponse"] = UNSET
    difficulty: Union[Unset, "DifficultyResponse"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        song: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.song, Unset):
            song = self.song.to_dict()

        difficulty: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.difficulty, Unset):
            difficulty = self.difficulty.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if song is not UNSET:
            field_dict["song"] = song
        if difficulty is not UNSET:
            field_dict["difficulty"] = difficulty

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.compact_song_response import CompactSongResponse
        from ..models.difficulty_response import DifficultyResponse

        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        _song = d.pop("song", UNSET)
        song: Union[Unset, CompactSongResponse]
        if isinstance(_song, Unset):
            song = UNSET
        else:
            song = CompactSongResponse.from_dict(_song)

        _difficulty = d.pop("difficulty", UNSET)
        difficulty: Union[Unset, DifficultyResponse]
        if isinstance(_difficulty, Unset):
            difficulty = UNSET
        else:
            difficulty = DifficultyResponse.from_dict(_difficulty)

        compact_leaderboard_response = cls(
            id=id,
            song=song,
            difficulty=difficulty,
        )

        return compact_leaderboard_response
