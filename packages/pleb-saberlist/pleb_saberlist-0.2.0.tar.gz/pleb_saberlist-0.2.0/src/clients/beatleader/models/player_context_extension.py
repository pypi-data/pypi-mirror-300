from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.leaderboard_contexts import LeaderboardContexts
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.player import Player
    from ..models.player_score_stats import PlayerScoreStats
    from ..models.player_search import PlayerSearch


T = TypeVar("T", bound="PlayerContextExtension")


@_attrs_define
class PlayerContextExtension:
    """
    Attributes:
        id (Union[Unset, int]):
        context (Union[Unset, LeaderboardContexts]):
        pp (Union[Unset, float]):
        acc_pp (Union[Unset, float]):
        tech_pp (Union[Unset, float]):
        pass_pp (Union[Unset, float]):
        rank (Union[Unset, int]):
        country (Union[None, Unset, str]):
        country_rank (Union[Unset, int]):
        last_week_pp (Union[Unset, float]):
        last_week_rank (Union[Unset, int]):
        last_week_country_rank (Union[Unset, int]):
        player_id (Union[None, Unset, str]):
        player_instance (Union[Unset, Player]):
        score_stats (Union[Unset, PlayerScoreStats]):
        banned (Union[Unset, bool]):
        searches (Union[List['PlayerSearch'], None, Unset]):
        name (Union[None, Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    context: Union[Unset, LeaderboardContexts] = UNSET
    pp: Union[Unset, float] = UNSET
    acc_pp: Union[Unset, float] = UNSET
    tech_pp: Union[Unset, float] = UNSET
    pass_pp: Union[Unset, float] = UNSET
    rank: Union[Unset, int] = UNSET
    country: Union[None, Unset, str] = UNSET
    country_rank: Union[Unset, int] = UNSET
    last_week_pp: Union[Unset, float] = UNSET
    last_week_rank: Union[Unset, int] = UNSET
    last_week_country_rank: Union[Unset, int] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    player_instance: Union[Unset, "Player"] = UNSET
    score_stats: Union[Unset, "PlayerScoreStats"] = UNSET
    banned: Union[Unset, bool] = UNSET
    searches: Union[List["PlayerSearch"], None, Unset] = UNSET
    name: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        context: Union[Unset, str] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.value

        pp = self.pp

        acc_pp = self.acc_pp

        tech_pp = self.tech_pp

        pass_pp = self.pass_pp

        rank = self.rank

        country: Union[None, Unset, str]
        if isinstance(self.country, Unset):
            country = UNSET
        else:
            country = self.country

        country_rank = self.country_rank

        last_week_pp = self.last_week_pp

        last_week_rank = self.last_week_rank

        last_week_country_rank = self.last_week_country_rank

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        player_instance: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.player_instance, Unset):
            player_instance = self.player_instance.to_dict()

        score_stats: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.score_stats, Unset):
            score_stats = self.score_stats.to_dict()

        banned = self.banned

        searches: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.searches, Unset):
            searches = UNSET
        elif isinstance(self.searches, list):
            searches = []
            for searches_type_0_item_data in self.searches:
                searches_type_0_item = searches_type_0_item_data.to_dict()
                searches.append(searches_type_0_item)

        else:
            searches = self.searches

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if context is not UNSET:
            field_dict["context"] = context
        if pp is not UNSET:
            field_dict["pp"] = pp
        if acc_pp is not UNSET:
            field_dict["accPp"] = acc_pp
        if tech_pp is not UNSET:
            field_dict["techPp"] = tech_pp
        if pass_pp is not UNSET:
            field_dict["passPp"] = pass_pp
        if rank is not UNSET:
            field_dict["rank"] = rank
        if country is not UNSET:
            field_dict["country"] = country
        if country_rank is not UNSET:
            field_dict["countryRank"] = country_rank
        if last_week_pp is not UNSET:
            field_dict["lastWeekPp"] = last_week_pp
        if last_week_rank is not UNSET:
            field_dict["lastWeekRank"] = last_week_rank
        if last_week_country_rank is not UNSET:
            field_dict["lastWeekCountryRank"] = last_week_country_rank
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if player_instance is not UNSET:
            field_dict["playerInstance"] = player_instance
        if score_stats is not UNSET:
            field_dict["scoreStats"] = score_stats
        if banned is not UNSET:
            field_dict["banned"] = banned
        if searches is not UNSET:
            field_dict["searches"] = searches
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.player import Player
        from ..models.player_score_stats import PlayerScoreStats
        from ..models.player_search import PlayerSearch

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _context = d.pop("context", UNSET)
        context: Union[Unset, LeaderboardContexts]
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = LeaderboardContexts(_context)

        pp = d.pop("pp", UNSET)

        acc_pp = d.pop("accPp", UNSET)

        tech_pp = d.pop("techPp", UNSET)

        pass_pp = d.pop("passPp", UNSET)

        rank = d.pop("rank", UNSET)

        def _parse_country(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        country = _parse_country(d.pop("country", UNSET))

        country_rank = d.pop("countryRank", UNSET)

        last_week_pp = d.pop("lastWeekPp", UNSET)

        last_week_rank = d.pop("lastWeekRank", UNSET)

        last_week_country_rank = d.pop("lastWeekCountryRank", UNSET)

        def _parse_player_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_id = _parse_player_id(d.pop("playerId", UNSET))

        _player_instance = d.pop("playerInstance", UNSET)
        player_instance: Union[Unset, Player]
        if isinstance(_player_instance, Unset):
            player_instance = UNSET
        else:
            player_instance = Player.from_dict(_player_instance)

        _score_stats = d.pop("scoreStats", UNSET)
        score_stats: Union[Unset, PlayerScoreStats]
        if isinstance(_score_stats, Unset):
            score_stats = UNSET
        else:
            score_stats = PlayerScoreStats.from_dict(_score_stats)

        banned = d.pop("banned", UNSET)

        def _parse_searches(data: object) -> Union[List["PlayerSearch"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                searches_type_0 = []
                _searches_type_0 = data
                for searches_type_0_item_data in _searches_type_0:
                    searches_type_0_item = PlayerSearch.from_dict(searches_type_0_item_data)

                    searches_type_0.append(searches_type_0_item)

                return searches_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["PlayerSearch"], None, Unset], data)

        searches = _parse_searches(d.pop("searches", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        player_context_extension = cls(
            id=id,
            context=context,
            pp=pp,
            acc_pp=acc_pp,
            tech_pp=tech_pp,
            pass_pp=pass_pp,
            rank=rank,
            country=country,
            country_rank=country_rank,
            last_week_pp=last_week_pp,
            last_week_rank=last_week_rank,
            last_week_country_rank=last_week_country_rank,
            player_id=player_id,
            player_instance=player_instance,
            score_stats=score_stats,
            banned=banned,
            searches=searches,
            name=name,
        )

        return player_context_extension
