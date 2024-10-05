import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.difficulty import Difficulty
    from ..models.score import Score


T = TypeVar("T", bound="LeaderboardInfo")


@_attrs_define
class LeaderboardInfo:
    """
    Attributes:
        id (float):
        song_hash (str):
        song_name (str):
        song_sub_name (str):
        song_author_name (str):
        level_author_name (str):
        difficulty (Difficulty):
        max_score (float):
        created_date (datetime.datetime):
        ranked_date (Union[None, datetime.datetime]):
        qualified_date (Union[None, datetime.datetime]):
        loved_date (Union[None, datetime.datetime]):
        ranked (bool):
        qualified (bool):
        loved (bool):
        max_pp (float):
        stars (float):
        positive_modifiers (bool):
        plays (float):
        daily_plays (float):
        cover_image (str):
        player_score (Union['Score', None]):
        difficulties (List['Difficulty']):
    """

    id: float
    song_hash: str
    song_name: str
    song_sub_name: str
    song_author_name: str
    level_author_name: str
    difficulty: "Difficulty"
    max_score: float
    created_date: datetime.datetime
    ranked_date: Union[None, datetime.datetime]
    qualified_date: Union[None, datetime.datetime]
    loved_date: Union[None, datetime.datetime]
    ranked: bool
    qualified: bool
    loved: bool
    max_pp: float
    stars: float
    positive_modifiers: bool
    plays: float
    daily_plays: float
    cover_image: str
    player_score: Union["Score", None]
    difficulties: List["Difficulty"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.score import Score

        id = self.id

        song_hash = self.song_hash

        song_name = self.song_name

        song_sub_name = self.song_sub_name

        song_author_name = self.song_author_name

        level_author_name = self.level_author_name

        difficulty = self.difficulty.to_dict()

        max_score = self.max_score

        created_date = self.created_date.isoformat()

        ranked_date: Union[None, str]
        if isinstance(self.ranked_date, datetime.datetime):
            ranked_date = self.ranked_date.isoformat()
        else:
            ranked_date = self.ranked_date

        qualified_date: Union[None, str]
        if isinstance(self.qualified_date, datetime.datetime):
            qualified_date = self.qualified_date.isoformat()
        else:
            qualified_date = self.qualified_date

        loved_date: Union[None, str]
        if isinstance(self.loved_date, datetime.datetime):
            loved_date = self.loved_date.isoformat()
        else:
            loved_date = self.loved_date

        ranked = self.ranked

        qualified = self.qualified

        loved = self.loved

        max_pp = self.max_pp

        stars = self.stars

        positive_modifiers = self.positive_modifiers

        plays = self.plays

        daily_plays = self.daily_plays

        cover_image = self.cover_image

        player_score: Union[Dict[str, Any], None]
        if isinstance(self.player_score, Score):
            player_score = self.player_score.to_dict()
        else:
            player_score = self.player_score

        difficulties = []
        for difficulties_item_data in self.difficulties:
            difficulties_item = difficulties_item_data.to_dict()
            difficulties.append(difficulties_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "songHash": song_hash,
                "songName": song_name,
                "songSubName": song_sub_name,
                "songAuthorName": song_author_name,
                "levelAuthorName": level_author_name,
                "difficulty": difficulty,
                "maxScore": max_score,
                "createdDate": created_date,
                "rankedDate": ranked_date,
                "qualifiedDate": qualified_date,
                "lovedDate": loved_date,
                "ranked": ranked,
                "qualified": qualified,
                "loved": loved,
                "maxPP": max_pp,
                "stars": stars,
                "positiveModifiers": positive_modifiers,
                "plays": plays,
                "dailyPlays": daily_plays,
                "coverImage": cover_image,
                "playerScore": player_score,
                "difficulties": difficulties,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.difficulty import Difficulty
        from ..models.score import Score

        d = src_dict.copy()
        id = d.pop("id")

        song_hash = d.pop("songHash")

        song_name = d.pop("songName")

        song_sub_name = d.pop("songSubName")

        song_author_name = d.pop("songAuthorName")

        level_author_name = d.pop("levelAuthorName")

        difficulty = Difficulty.from_dict(d.pop("difficulty"))

        max_score = d.pop("maxScore")

        created_date = isoparse(d.pop("createdDate"))

        def _parse_ranked_date(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ranked_date_type_0 = isoparse(data)

                return ranked_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        ranked_date = _parse_ranked_date(d.pop("rankedDate"))

        def _parse_qualified_date(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                qualified_date_type_0 = isoparse(data)

                return qualified_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        qualified_date = _parse_qualified_date(d.pop("qualifiedDate"))

        def _parse_loved_date(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                loved_date_type_0 = isoparse(data)

                return loved_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        loved_date = _parse_loved_date(d.pop("lovedDate"))

        ranked = d.pop("ranked")

        qualified = d.pop("qualified")

        loved = d.pop("loved")

        max_pp = d.pop("maxPP")

        stars = d.pop("stars")

        positive_modifiers = d.pop("positiveModifiers")

        plays = d.pop("plays")

        daily_plays = d.pop("dailyPlays")

        cover_image = d.pop("coverImage")

        def _parse_player_score(data: object) -> Union["Score", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                player_score_type_1 = Score.from_dict(data)

                return player_score_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Score", None], data)

        player_score = _parse_player_score(d.pop("playerScore"))

        _difficulties = d.pop("difficulties", None)
        difficulties = []
        if _difficulties is not None:
            for difficulties_item_data in _difficulties:
                difficulties_item = Difficulty.from_dict(difficulties_item_data)
                difficulties.append(difficulties_item)
        else:
            difficulties = []

        leaderboard_info = cls(
            id=id,
            song_hash=song_hash,
            song_name=song_name,
            song_sub_name=song_sub_name,
            song_author_name=song_author_name,
            level_author_name=level_author_name,
            difficulty=difficulty,
            max_score=max_score,
            created_date=created_date,
            ranked_date=ranked_date,
            qualified_date=qualified_date,
            loved_date=loved_date,
            ranked=ranked,
            qualified=qualified,
            loved=loved,
            max_pp=max_pp,
            stars=stars,
            positive_modifiers=positive_modifiers,
            plays=plays,
            daily_plays=daily_plays,
            cover_image=cover_image,
            player_score=player_score,
            difficulties=difficulties,
        )

        leaderboard_info.additional_properties = d
        return leaderboard_info

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
