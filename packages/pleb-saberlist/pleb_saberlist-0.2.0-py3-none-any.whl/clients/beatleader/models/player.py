from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.achievement import Achievement
    from ..models.badge import Badge
    from ..models.event_player import EventPlayer
    from ..models.mapper import Mapper
    from ..models.patreon_features import PatreonFeatures
    from ..models.player_change import PlayerChange
    from ..models.player_score_stats import PlayerScoreStats
    from ..models.player_score_stats_history import PlayerScoreStatsHistory
    from ..models.player_social import PlayerSocial
    from ..models.profile_settings import ProfileSettings


T = TypeVar("T", bound="Player")


@_attrs_define
class Player:
    """
    Attributes:
        id (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        platform (Union[None, Unset, str]):
        avatar (Union[None, Unset, str]):
        web_avatar (Union[None, Unset, str]):
        country (Union[None, Unset, str]):
        alias (Union[None, Unset, str]):
        old_alias (Union[None, Unset, str]):
        role (Union[None, Unset, str]):
        mapper_id (Union[None, Unset, int]):
        mapper (Union[Unset, Mapper]):
        pp (Union[Unset, float]):
        acc_pp (Union[Unset, float]):
        tech_pp (Union[Unset, float]):
        pass_pp (Union[Unset, float]):
        rank (Union[Unset, int]):
        country_rank (Union[Unset, int]):
        last_week_pp (Union[Unset, float]):
        last_week_rank (Union[Unset, int]):
        last_week_country_rank (Union[Unset, int]):
        banned (Union[Unset, bool]):
        bot (Union[Unset, bool]):
        inactive (Union[Unset, bool]):
        external_profile_url (Union[None, Unset, str]):
        rich_bio_timeset (Union[Unset, int]):
        created_at (Union[Unset, int]):
        speedrun_start (Union[Unset, int]):
        score_stats_id (Union[None, Unset, int]):
        score_stats (Union[Unset, PlayerScoreStats]):
        clan_order (Union[None, Unset, str]):
        badges (Union[List['Badge'], None, Unset]):
        patreon_features (Union[Unset, PatreonFeatures]):
        profile_settings (Union[Unset, ProfileSettings]):
        changes (Union[List['PlayerChange'], None, Unset]):
        history (Union[List['PlayerScoreStatsHistory'], None, Unset]):
        events_participating (Union[List['EventPlayer'], None, Unset]):
        socials (Union[List['PlayerSocial'], None, Unset]):
        achievements (Union[List['Achievement'], None, Unset]):
    """

    id: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    platform: Union[None, Unset, str] = UNSET
    avatar: Union[None, Unset, str] = UNSET
    web_avatar: Union[None, Unset, str] = UNSET
    country: Union[None, Unset, str] = UNSET
    alias: Union[None, Unset, str] = UNSET
    old_alias: Union[None, Unset, str] = UNSET
    role: Union[None, Unset, str] = UNSET
    mapper_id: Union[None, Unset, int] = UNSET
    mapper: Union[Unset, "Mapper"] = UNSET
    pp: Union[Unset, float] = UNSET
    acc_pp: Union[Unset, float] = UNSET
    tech_pp: Union[Unset, float] = UNSET
    pass_pp: Union[Unset, float] = UNSET
    rank: Union[Unset, int] = UNSET
    country_rank: Union[Unset, int] = UNSET
    last_week_pp: Union[Unset, float] = UNSET
    last_week_rank: Union[Unset, int] = UNSET
    last_week_country_rank: Union[Unset, int] = UNSET
    banned: Union[Unset, bool] = UNSET
    bot: Union[Unset, bool] = UNSET
    inactive: Union[Unset, bool] = UNSET
    external_profile_url: Union[None, Unset, str] = UNSET
    rich_bio_timeset: Union[Unset, int] = UNSET
    created_at: Union[Unset, int] = UNSET
    speedrun_start: Union[Unset, int] = UNSET
    score_stats_id: Union[None, Unset, int] = UNSET
    score_stats: Union[Unset, "PlayerScoreStats"] = UNSET
    clan_order: Union[None, Unset, str] = UNSET
    badges: Union[List["Badge"], None, Unset] = UNSET
    patreon_features: Union[Unset, "PatreonFeatures"] = UNSET
    profile_settings: Union[Unset, "ProfileSettings"] = UNSET
    changes: Union[List["PlayerChange"], None, Unset] = UNSET
    history: Union[List["PlayerScoreStatsHistory"], None, Unset] = UNSET
    events_participating: Union[List["EventPlayer"], None, Unset] = UNSET
    socials: Union[List["PlayerSocial"], None, Unset] = UNSET
    achievements: Union[List["Achievement"], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        platform: Union[None, Unset, str]
        if isinstance(self.platform, Unset):
            platform = UNSET
        else:
            platform = self.platform

        avatar: Union[None, Unset, str]
        if isinstance(self.avatar, Unset):
            avatar = UNSET
        else:
            avatar = self.avatar

        web_avatar: Union[None, Unset, str]
        if isinstance(self.web_avatar, Unset):
            web_avatar = UNSET
        else:
            web_avatar = self.web_avatar

        country: Union[None, Unset, str]
        if isinstance(self.country, Unset):
            country = UNSET
        else:
            country = self.country

        alias: Union[None, Unset, str]
        if isinstance(self.alias, Unset):
            alias = UNSET
        else:
            alias = self.alias

        old_alias: Union[None, Unset, str]
        if isinstance(self.old_alias, Unset):
            old_alias = UNSET
        else:
            old_alias = self.old_alias

        role: Union[None, Unset, str]
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        mapper_id: Union[None, Unset, int]
        if isinstance(self.mapper_id, Unset):
            mapper_id = UNSET
        else:
            mapper_id = self.mapper_id

        mapper: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.mapper, Unset):
            mapper = self.mapper.to_dict()

        pp = self.pp

        acc_pp = self.acc_pp

        tech_pp = self.tech_pp

        pass_pp = self.pass_pp

        rank = self.rank

        country_rank = self.country_rank

        last_week_pp = self.last_week_pp

        last_week_rank = self.last_week_rank

        last_week_country_rank = self.last_week_country_rank

        banned = self.banned

        bot = self.bot

        inactive = self.inactive

        external_profile_url: Union[None, Unset, str]
        if isinstance(self.external_profile_url, Unset):
            external_profile_url = UNSET
        else:
            external_profile_url = self.external_profile_url

        rich_bio_timeset = self.rich_bio_timeset

        created_at = self.created_at

        speedrun_start = self.speedrun_start

        score_stats_id: Union[None, Unset, int]
        if isinstance(self.score_stats_id, Unset):
            score_stats_id = UNSET
        else:
            score_stats_id = self.score_stats_id

        score_stats: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.score_stats, Unset):
            score_stats = self.score_stats.to_dict()

        clan_order: Union[None, Unset, str]
        if isinstance(self.clan_order, Unset):
            clan_order = UNSET
        else:
            clan_order = self.clan_order

        badges: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.badges, Unset):
            badges = UNSET
        elif isinstance(self.badges, list):
            badges = []
            for badges_type_0_item_data in self.badges:
                badges_type_0_item = badges_type_0_item_data.to_dict()
                badges.append(badges_type_0_item)

        else:
            badges = self.badges

        patreon_features: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.patreon_features, Unset):
            patreon_features = self.patreon_features.to_dict()

        profile_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profile_settings, Unset):
            profile_settings = self.profile_settings.to_dict()

        changes: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.changes, Unset):
            changes = UNSET
        elif isinstance(self.changes, list):
            changes = []
            for changes_type_0_item_data in self.changes:
                changes_type_0_item = changes_type_0_item_data.to_dict()
                changes.append(changes_type_0_item)

        else:
            changes = self.changes

        history: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.history, Unset):
            history = UNSET
        elif isinstance(self.history, list):
            history = []
            for history_type_0_item_data in self.history:
                history_type_0_item = history_type_0_item_data.to_dict()
                history.append(history_type_0_item)

        else:
            history = self.history

        events_participating: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.events_participating, Unset):
            events_participating = UNSET
        elif isinstance(self.events_participating, list):
            events_participating = []
            for events_participating_type_0_item_data in self.events_participating:
                events_participating_type_0_item = events_participating_type_0_item_data.to_dict()
                events_participating.append(events_participating_type_0_item)

        else:
            events_participating = self.events_participating

        socials: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.socials, Unset):
            socials = UNSET
        elif isinstance(self.socials, list):
            socials = []
            for socials_type_0_item_data in self.socials:
                socials_type_0_item = socials_type_0_item_data.to_dict()
                socials.append(socials_type_0_item)

        else:
            socials = self.socials

        achievements: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.achievements, Unset):
            achievements = UNSET
        elif isinstance(self.achievements, list):
            achievements = []
            for achievements_type_0_item_data in self.achievements:
                achievements_type_0_item = achievements_type_0_item_data.to_dict()
                achievements.append(achievements_type_0_item)

        else:
            achievements = self.achievements

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if platform is not UNSET:
            field_dict["platform"] = platform
        if avatar is not UNSET:
            field_dict["avatar"] = avatar
        if web_avatar is not UNSET:
            field_dict["webAvatar"] = web_avatar
        if country is not UNSET:
            field_dict["country"] = country
        if alias is not UNSET:
            field_dict["alias"] = alias
        if old_alias is not UNSET:
            field_dict["oldAlias"] = old_alias
        if role is not UNSET:
            field_dict["role"] = role
        if mapper_id is not UNSET:
            field_dict["mapperId"] = mapper_id
        if mapper is not UNSET:
            field_dict["mapper"] = mapper
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
        if country_rank is not UNSET:
            field_dict["countryRank"] = country_rank
        if last_week_pp is not UNSET:
            field_dict["lastWeekPp"] = last_week_pp
        if last_week_rank is not UNSET:
            field_dict["lastWeekRank"] = last_week_rank
        if last_week_country_rank is not UNSET:
            field_dict["lastWeekCountryRank"] = last_week_country_rank
        if banned is not UNSET:
            field_dict["banned"] = banned
        if bot is not UNSET:
            field_dict["bot"] = bot
        if inactive is not UNSET:
            field_dict["inactive"] = inactive
        if external_profile_url is not UNSET:
            field_dict["externalProfileUrl"] = external_profile_url
        if rich_bio_timeset is not UNSET:
            field_dict["richBioTimeset"] = rich_bio_timeset
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if speedrun_start is not UNSET:
            field_dict["speedrunStart"] = speedrun_start
        if score_stats_id is not UNSET:
            field_dict["scoreStatsId"] = score_stats_id
        if score_stats is not UNSET:
            field_dict["scoreStats"] = score_stats
        if clan_order is not UNSET:
            field_dict["clanOrder"] = clan_order
        if badges is not UNSET:
            field_dict["badges"] = badges
        if patreon_features is not UNSET:
            field_dict["patreonFeatures"] = patreon_features
        if profile_settings is not UNSET:
            field_dict["profileSettings"] = profile_settings
        if changes is not UNSET:
            field_dict["changes"] = changes
        if history is not UNSET:
            field_dict["history"] = history
        if events_participating is not UNSET:
            field_dict["eventsParticipating"] = events_participating
        if socials is not UNSET:
            field_dict["socials"] = socials
        if achievements is not UNSET:
            field_dict["achievements"] = achievements

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.achievement import Achievement
        from ..models.badge import Badge
        from ..models.event_player import EventPlayer
        from ..models.mapper import Mapper
        from ..models.patreon_features import PatreonFeatures
        from ..models.player_change import PlayerChange
        from ..models.player_score_stats import PlayerScoreStats
        from ..models.player_score_stats_history import PlayerScoreStatsHistory
        from ..models.player_social import PlayerSocial
        from ..models.profile_settings import ProfileSettings

        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_platform(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        platform = _parse_platform(d.pop("platform", UNSET))

        def _parse_avatar(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        avatar = _parse_avatar(d.pop("avatar", UNSET))

        def _parse_web_avatar(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        web_avatar = _parse_web_avatar(d.pop("webAvatar", UNSET))

        def _parse_country(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        country = _parse_country(d.pop("country", UNSET))

        def _parse_alias(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        alias = _parse_alias(d.pop("alias", UNSET))

        def _parse_old_alias(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        old_alias = _parse_old_alias(d.pop("oldAlias", UNSET))

        def _parse_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_mapper_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        mapper_id = _parse_mapper_id(d.pop("mapperId", UNSET))

        _mapper = d.pop("mapper", UNSET)
        mapper: Union[Unset, Mapper]
        if isinstance(_mapper, Unset):
            mapper = UNSET
        else:
            mapper = Mapper.from_dict(_mapper)

        pp = d.pop("pp", UNSET)

        acc_pp = d.pop("accPp", UNSET)

        tech_pp = d.pop("techPp", UNSET)

        pass_pp = d.pop("passPp", UNSET)

        rank = d.pop("rank", UNSET)

        country_rank = d.pop("countryRank", UNSET)

        last_week_pp = d.pop("lastWeekPp", UNSET)

        last_week_rank = d.pop("lastWeekRank", UNSET)

        last_week_country_rank = d.pop("lastWeekCountryRank", UNSET)

        banned = d.pop("banned", UNSET)

        bot = d.pop("bot", UNSET)

        inactive = d.pop("inactive", UNSET)

        def _parse_external_profile_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_profile_url = _parse_external_profile_url(d.pop("externalProfileUrl", UNSET))

        rich_bio_timeset = d.pop("richBioTimeset", UNSET)

        created_at = d.pop("createdAt", UNSET)

        speedrun_start = d.pop("speedrunStart", UNSET)

        def _parse_score_stats_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        score_stats_id = _parse_score_stats_id(d.pop("scoreStatsId", UNSET))

        _score_stats = d.pop("scoreStats", UNSET)
        score_stats: Union[Unset, PlayerScoreStats]
        if isinstance(_score_stats, Unset):
            score_stats = UNSET
        else:
            score_stats = PlayerScoreStats.from_dict(_score_stats)

        def _parse_clan_order(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        clan_order = _parse_clan_order(d.pop("clanOrder", UNSET))

        def _parse_badges(data: object) -> Union[List["Badge"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                badges_type_0 = []
                _badges_type_0 = data
                for badges_type_0_item_data in _badges_type_0:
                    badges_type_0_item = Badge.from_dict(badges_type_0_item_data)

                    badges_type_0.append(badges_type_0_item)

                return badges_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["Badge"], None, Unset], data)

        badges = _parse_badges(d.pop("badges", UNSET))

        _patreon_features = d.pop("patreonFeatures", UNSET)
        patreon_features: Union[Unset, PatreonFeatures]
        if isinstance(_patreon_features, Unset):
            patreon_features = UNSET
        else:
            patreon_features = PatreonFeatures.from_dict(_patreon_features)

        _profile_settings = d.pop("profileSettings", UNSET)
        profile_settings: Union[Unset, ProfileSettings]
        if isinstance(_profile_settings, Unset):
            profile_settings = UNSET
        else:
            profile_settings = ProfileSettings.from_dict(_profile_settings)

        def _parse_changes(data: object) -> Union[List["PlayerChange"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                changes_type_0 = []
                _changes_type_0 = data
                for changes_type_0_item_data in _changes_type_0:
                    changes_type_0_item = PlayerChange.from_dict(changes_type_0_item_data)

                    changes_type_0.append(changes_type_0_item)

                return changes_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["PlayerChange"], None, Unset], data)

        changes = _parse_changes(d.pop("changes", UNSET))

        def _parse_history(data: object) -> Union[List["PlayerScoreStatsHistory"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                history_type_0 = []
                _history_type_0 = data
                for history_type_0_item_data in _history_type_0:
                    history_type_0_item = PlayerScoreStatsHistory.from_dict(history_type_0_item_data)

                    history_type_0.append(history_type_0_item)

                return history_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["PlayerScoreStatsHistory"], None, Unset], data)

        history = _parse_history(d.pop("history", UNSET))

        def _parse_events_participating(data: object) -> Union[List["EventPlayer"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                events_participating_type_0 = []
                _events_participating_type_0 = data
                for events_participating_type_0_item_data in _events_participating_type_0:
                    events_participating_type_0_item = EventPlayer.from_dict(events_participating_type_0_item_data)

                    events_participating_type_0.append(events_participating_type_0_item)

                return events_participating_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["EventPlayer"], None, Unset], data)

        events_participating = _parse_events_participating(d.pop("eventsParticipating", UNSET))

        def _parse_socials(data: object) -> Union[List["PlayerSocial"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                socials_type_0 = []
                _socials_type_0 = data
                for socials_type_0_item_data in _socials_type_0:
                    socials_type_0_item = PlayerSocial.from_dict(socials_type_0_item_data)

                    socials_type_0.append(socials_type_0_item)

                return socials_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["PlayerSocial"], None, Unset], data)

        socials = _parse_socials(d.pop("socials", UNSET))

        def _parse_achievements(data: object) -> Union[List["Achievement"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                achievements_type_0 = []
                _achievements_type_0 = data
                for achievements_type_0_item_data in _achievements_type_0:
                    achievements_type_0_item = Achievement.from_dict(achievements_type_0_item_data)

                    achievements_type_0.append(achievements_type_0_item)

                return achievements_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["Achievement"], None, Unset], data)

        achievements = _parse_achievements(d.pop("achievements", UNSET))

        player = cls(
            id=id,
            name=name,
            platform=platform,
            avatar=avatar,
            web_avatar=web_avatar,
            country=country,
            alias=alias,
            old_alias=old_alias,
            role=role,
            mapper_id=mapper_id,
            mapper=mapper,
            pp=pp,
            acc_pp=acc_pp,
            tech_pp=tech_pp,
            pass_pp=pass_pp,
            rank=rank,
            country_rank=country_rank,
            last_week_pp=last_week_pp,
            last_week_rank=last_week_rank,
            last_week_country_rank=last_week_country_rank,
            banned=banned,
            bot=bot,
            inactive=inactive,
            external_profile_url=external_profile_url,
            rich_bio_timeset=rich_bio_timeset,
            created_at=created_at,
            speedrun_start=speedrun_start,
            score_stats_id=score_stats_id,
            score_stats=score_stats,
            clan_order=clan_order,
            badges=badges,
            patreon_features=patreon_features,
            profile_settings=profile_settings,
            changes=changes,
            history=history,
            events_participating=events_participating,
            socials=socials,
            achievements=achievements,
        )

        return player
