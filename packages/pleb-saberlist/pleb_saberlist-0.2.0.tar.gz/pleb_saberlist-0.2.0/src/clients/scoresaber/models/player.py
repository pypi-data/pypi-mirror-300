import datetime
from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.player_badges_type_1 import PlayerBadgesType1
    from ..models.score_stats import ScoreStats


T = TypeVar("T", bound="Player")


@_attrs_define
class Player:
    """
    Attributes:
        id (str):
        name (str):
        profile_picture (str):
        bio (Union[None, str]):
        country (str):
        pp (float):
        rank (float):
        country_rank (float):
        role (str):
        badges (Union['PlayerBadgesType1', None]):
        histories (str):
        score_stats (Union['ScoreStats', None]):
        permissions (float):
        banned (bool):
        inactive (bool):
        first_seen (Union[None, datetime.datetime]):
    """

    id: str
    name: str
    profile_picture: str
    bio: Union[None, str]
    country: str
    pp: float
    rank: float
    country_rank: float
    role: str
    badges: Union["PlayerBadgesType1", None]
    histories: str
    score_stats: Union["ScoreStats", None]
    permissions: float
    banned: bool
    inactive: bool
    first_seen: Union[None, datetime.datetime]

    def to_dict(self) -> Dict[str, Any]:
        from ..models.player_badges_type_1 import PlayerBadgesType1
        from ..models.score_stats import ScoreStats

        id = self.id

        name = self.name

        profile_picture = self.profile_picture

        bio: Union[None, str]
        bio = self.bio

        country = self.country

        pp = self.pp

        rank = self.rank

        country_rank = self.country_rank

        role = self.role

        badges: Union[Dict[str, Any], None]
        if isinstance(self.badges, PlayerBadgesType1):
            badges = self.badges.to_dict()
        else:
            badges = self.badges

        histories = self.histories

        score_stats: Union[Dict[str, Any], None]
        if isinstance(self.score_stats, ScoreStats):
            score_stats = self.score_stats.to_dict()
        else:
            score_stats = self.score_stats

        permissions = self.permissions

        banned = self.banned

        inactive = self.inactive

        first_seen: Union[None, str]
        if isinstance(self.first_seen, datetime.datetime):
            first_seen = self.first_seen.isoformat()
        else:
            first_seen = self.first_seen

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "profilePicture": profile_picture,
                "bio": bio,
                "country": country,
                "pp": pp,
                "rank": rank,
                "countryRank": country_rank,
                "role": role,
                "badges": badges,
                "histories": histories,
                "scoreStats": score_stats,
                "permissions": permissions,
                "banned": banned,
                "inactive": inactive,
                "firstSeen": first_seen,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.player_badges_type_1 import PlayerBadgesType1
        from ..models.score_stats import ScoreStats

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        profile_picture = d.pop("profilePicture")

        def _parse_bio(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        bio = _parse_bio(d.pop("bio"))

        country = d.pop("country")

        pp = d.pop("pp")

        rank = d.pop("rank")

        country_rank = d.pop("countryRank")

        role = d.pop("role")

        def _parse_badges(data: object) -> Union["PlayerBadgesType1", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                badges_type_1 = PlayerBadgesType1.from_dict(data)

                return badges_type_1
            except:  # noqa: E722
                pass
            return cast(Union["PlayerBadgesType1", None], data)

        badges = _parse_badges(d.pop("badges"))

        histories = d.pop("histories")

        def _parse_score_stats(data: object) -> Union["ScoreStats", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                score_stats_type_1 = ScoreStats.from_dict(data)

                return score_stats_type_1
            except:  # noqa: E722
                pass
            return cast(Union["ScoreStats", None], data)

        score_stats = _parse_score_stats(d.pop("scoreStats"))

        permissions = d.pop("permissions")

        banned = d.pop("banned")

        inactive = d.pop("inactive")

        def _parse_first_seen(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_seen_type_0 = isoparse(data)

                return first_seen_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        first_seen = _parse_first_seen(d.pop("firstSeen"))

        player = cls(
            id=id,
            name=name,
            profile_picture=profile_picture,
            bio=bio,
            country=country,
            pp=pp,
            rank=rank,
            country_rank=country_rank,
            role=role,
            badges=badges,
            histories=histories,
            score_stats=score_stats,
            permissions=permissions,
            banned=banned,
            inactive=inactive,
            first_seen=first_seen,
        )

        return player
