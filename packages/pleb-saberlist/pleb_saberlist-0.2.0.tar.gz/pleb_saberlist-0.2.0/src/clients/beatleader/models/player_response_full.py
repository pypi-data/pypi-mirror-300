from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.badge import Badge
    from ..models.ban import Ban
    from ..models.clan_response import ClanResponse
    from ..models.link_response import LinkResponse
    from ..models.patreon_features import PatreonFeatures
    from ..models.player_change import PlayerChange
    from ..models.player_context_extension import PlayerContextExtension
    from ..models.player_score_stats import PlayerScoreStats
    from ..models.player_score_stats_history import PlayerScoreStatsHistory
    from ..models.player_social import PlayerSocial
    from ..models.profile_settings import ProfileSettings
    from ..models.score_response_with_my_score import ScoreResponseWithMyScore


T = TypeVar("T", bound="PlayerResponseFull")


@_attrs_define
class PlayerResponseFull:
    """
    Attributes:
        id (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        platform (Union[None, Unset, str]):
        avatar (Union[None, Unset, str]):
        country (Union[None, Unset, str]):
        alias (Union[None, Unset, str]):
        bot (Union[Unset, bool]):
        pp (Union[Unset, float]):
        rank (Union[Unset, int]):
        country_rank (Union[Unset, int]):
        role (Union[None, Unset, str]):
        socials (Union[List['PlayerSocial'], None, Unset]):
        context_extensions (Union[List['PlayerContextExtension'], None, Unset]):
        patreon_features (Union[Unset, PatreonFeatures]):
        profile_settings (Union[Unset, ProfileSettings]):
        clan_order (Union[None, Unset, str]):
        clans (Union[List['ClanResponse'], None, Unset]):
        acc_pp (Union[Unset, float]):
        pass_pp (Union[Unset, float]):
        tech_pp (Union[Unset, float]):
        score_stats (Union[Unset, PlayerScoreStats]):
        last_week_pp (Union[Unset, float]):
        last_week_rank (Union[Unset, int]):
        last_week_country_rank (Union[Unset, int]):
        extension_id (Union[Unset, int]):
        mapper_id (Union[Unset, int]):
        banned (Union[Unset, bool]):
        inactive (Union[Unset, bool]):
        ban_description (Union[Unset, Ban]):
        external_profile_url (Union[None, Unset, str]):
        rich_bio_timeset (Union[Unset, int]):
        speedrun_start (Union[Unset, int]):
        linked_ids (Union[Unset, LinkResponse]):
        history (Union[List['PlayerScoreStatsHistory'], None, Unset]):
        badges (Union[List['Badge'], None, Unset]):
        pinned_scores (Union[List['ScoreResponseWithMyScore'], None, Unset]):
        changes (Union[List['PlayerChange'], None, Unset]):
    """

    id: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    platform: Union[None, Unset, str] = UNSET
    avatar: Union[None, Unset, str] = UNSET
    country: Union[None, Unset, str] = UNSET
    alias: Union[None, Unset, str] = UNSET
    bot: Union[Unset, bool] = UNSET
    pp: Union[Unset, float] = UNSET
    rank: Union[Unset, int] = UNSET
    country_rank: Union[Unset, int] = UNSET
    role: Union[None, Unset, str] = UNSET
    socials: Union[List["PlayerSocial"], None, Unset] = UNSET
    context_extensions: Union[List["PlayerContextExtension"], None, Unset] = UNSET
    patreon_features: Union[Unset, "PatreonFeatures"] = UNSET
    profile_settings: Union[Unset, "ProfileSettings"] = UNSET
    clan_order: Union[None, Unset, str] = UNSET
    clans: Union[List["ClanResponse"], None, Unset] = UNSET
    acc_pp: Union[Unset, float] = UNSET
    pass_pp: Union[Unset, float] = UNSET
    tech_pp: Union[Unset, float] = UNSET
    score_stats: Union[Unset, "PlayerScoreStats"] = UNSET
    last_week_pp: Union[Unset, float] = UNSET
    last_week_rank: Union[Unset, int] = UNSET
    last_week_country_rank: Union[Unset, int] = UNSET
    extension_id: Union[Unset, int] = UNSET
    mapper_id: Union[Unset, int] = UNSET
    banned: Union[Unset, bool] = UNSET
    inactive: Union[Unset, bool] = UNSET
    ban_description: Union[Unset, "Ban"] = UNSET
    external_profile_url: Union[None, Unset, str] = UNSET
    rich_bio_timeset: Union[Unset, int] = UNSET
    speedrun_start: Union[Unset, int] = UNSET
    linked_ids: Union[Unset, "LinkResponse"] = UNSET
    history: Union[List["PlayerScoreStatsHistory"], None, Unset] = UNSET
    badges: Union[List["Badge"], None, Unset] = UNSET
    pinned_scores: Union[List["ScoreResponseWithMyScore"], None, Unset] = UNSET
    changes: Union[List["PlayerChange"], None, Unset] = UNSET

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

        bot = self.bot

        pp = self.pp

        rank = self.rank

        country_rank = self.country_rank

        role: Union[None, Unset, str]
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

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

        context_extensions: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.context_extensions, Unset):
            context_extensions = UNSET
        elif isinstance(self.context_extensions, list):
            context_extensions = []
            for context_extensions_type_0_item_data in self.context_extensions:
                context_extensions_type_0_item = context_extensions_type_0_item_data.to_dict()
                context_extensions.append(context_extensions_type_0_item)

        else:
            context_extensions = self.context_extensions

        patreon_features: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.patreon_features, Unset):
            patreon_features = self.patreon_features.to_dict()

        profile_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profile_settings, Unset):
            profile_settings = self.profile_settings.to_dict()

        clan_order: Union[None, Unset, str]
        if isinstance(self.clan_order, Unset):
            clan_order = UNSET
        else:
            clan_order = self.clan_order

        clans: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.clans, Unset):
            clans = UNSET
        elif isinstance(self.clans, list):
            clans = []
            for clans_type_0_item_data in self.clans:
                clans_type_0_item = clans_type_0_item_data.to_dict()
                clans.append(clans_type_0_item)

        else:
            clans = self.clans

        acc_pp = self.acc_pp

        pass_pp = self.pass_pp

        tech_pp = self.tech_pp

        score_stats: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.score_stats, Unset):
            score_stats = self.score_stats.to_dict()

        last_week_pp = self.last_week_pp

        last_week_rank = self.last_week_rank

        last_week_country_rank = self.last_week_country_rank

        extension_id = self.extension_id

        mapper_id = self.mapper_id

        banned = self.banned

        inactive = self.inactive

        ban_description: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ban_description, Unset):
            ban_description = self.ban_description.to_dict()

        external_profile_url: Union[None, Unset, str]
        if isinstance(self.external_profile_url, Unset):
            external_profile_url = UNSET
        else:
            external_profile_url = self.external_profile_url

        rich_bio_timeset = self.rich_bio_timeset

        speedrun_start = self.speedrun_start

        linked_ids: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.linked_ids, Unset):
            linked_ids = self.linked_ids.to_dict()

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

        pinned_scores: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.pinned_scores, Unset):
            pinned_scores = UNSET
        elif isinstance(self.pinned_scores, list):
            pinned_scores = []
            for pinned_scores_type_0_item_data in self.pinned_scores:
                pinned_scores_type_0_item = pinned_scores_type_0_item_data.to_dict()
                pinned_scores.append(pinned_scores_type_0_item)

        else:
            pinned_scores = self.pinned_scores

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
        if country is not UNSET:
            field_dict["country"] = country
        if alias is not UNSET:
            field_dict["alias"] = alias
        if bot is not UNSET:
            field_dict["bot"] = bot
        if pp is not UNSET:
            field_dict["pp"] = pp
        if rank is not UNSET:
            field_dict["rank"] = rank
        if country_rank is not UNSET:
            field_dict["countryRank"] = country_rank
        if role is not UNSET:
            field_dict["role"] = role
        if socials is not UNSET:
            field_dict["socials"] = socials
        if context_extensions is not UNSET:
            field_dict["contextExtensions"] = context_extensions
        if patreon_features is not UNSET:
            field_dict["patreonFeatures"] = patreon_features
        if profile_settings is not UNSET:
            field_dict["profileSettings"] = profile_settings
        if clan_order is not UNSET:
            field_dict["clanOrder"] = clan_order
        if clans is not UNSET:
            field_dict["clans"] = clans
        if acc_pp is not UNSET:
            field_dict["accPp"] = acc_pp
        if pass_pp is not UNSET:
            field_dict["passPp"] = pass_pp
        if tech_pp is not UNSET:
            field_dict["techPp"] = tech_pp
        if score_stats is not UNSET:
            field_dict["scoreStats"] = score_stats
        if last_week_pp is not UNSET:
            field_dict["lastWeekPp"] = last_week_pp
        if last_week_rank is not UNSET:
            field_dict["lastWeekRank"] = last_week_rank
        if last_week_country_rank is not UNSET:
            field_dict["lastWeekCountryRank"] = last_week_country_rank
        if extension_id is not UNSET:
            field_dict["extensionId"] = extension_id
        if mapper_id is not UNSET:
            field_dict["mapperId"] = mapper_id
        if banned is not UNSET:
            field_dict["banned"] = banned
        if inactive is not UNSET:
            field_dict["inactive"] = inactive
        if ban_description is not UNSET:
            field_dict["banDescription"] = ban_description
        if external_profile_url is not UNSET:
            field_dict["externalProfileUrl"] = external_profile_url
        if rich_bio_timeset is not UNSET:
            field_dict["richBioTimeset"] = rich_bio_timeset
        if speedrun_start is not UNSET:
            field_dict["speedrunStart"] = speedrun_start
        if linked_ids is not UNSET:
            field_dict["linkedIds"] = linked_ids
        if history is not UNSET:
            field_dict["history"] = history
        if badges is not UNSET:
            field_dict["badges"] = badges
        if pinned_scores is not UNSET:
            field_dict["pinnedScores"] = pinned_scores
        if changes is not UNSET:
            field_dict["changes"] = changes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.badge import Badge
        from ..models.ban import Ban
        from ..models.clan_response import ClanResponse
        from ..models.link_response import LinkResponse
        from ..models.patreon_features import PatreonFeatures
        from ..models.player_change import PlayerChange
        from ..models.player_context_extension import PlayerContextExtension
        from ..models.player_score_stats import PlayerScoreStats
        from ..models.player_score_stats_history import PlayerScoreStatsHistory
        from ..models.player_social import PlayerSocial
        from ..models.profile_settings import ProfileSettings
        from ..models.score_response_with_my_score import ScoreResponseWithMyScore

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

        bot = d.pop("bot", UNSET)

        pp = d.pop("pp", UNSET)

        rank = d.pop("rank", UNSET)

        country_rank = d.pop("countryRank", UNSET)

        def _parse_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        role = _parse_role(d.pop("role", UNSET))

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

        def _parse_context_extensions(data: object) -> Union[List["PlayerContextExtension"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                context_extensions_type_0 = []
                _context_extensions_type_0 = data
                for context_extensions_type_0_item_data in _context_extensions_type_0:
                    context_extensions_type_0_item = PlayerContextExtension.from_dict(
                        context_extensions_type_0_item_data
                    )

                    context_extensions_type_0.append(context_extensions_type_0_item)

                return context_extensions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["PlayerContextExtension"], None, Unset], data)

        context_extensions = _parse_context_extensions(d.pop("contextExtensions", UNSET))

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

        def _parse_clan_order(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        clan_order = _parse_clan_order(d.pop("clanOrder", UNSET))

        def _parse_clans(data: object) -> Union[List["ClanResponse"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                clans_type_0 = []
                _clans_type_0 = data
                for clans_type_0_item_data in _clans_type_0:
                    clans_type_0_item = ClanResponse.from_dict(clans_type_0_item_data)

                    clans_type_0.append(clans_type_0_item)

                return clans_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ClanResponse"], None, Unset], data)

        clans = _parse_clans(d.pop("clans", UNSET))

        acc_pp = d.pop("accPp", UNSET)

        pass_pp = d.pop("passPp", UNSET)

        tech_pp = d.pop("techPp", UNSET)

        _score_stats = d.pop("scoreStats", UNSET)
        score_stats: Union[Unset, PlayerScoreStats]
        if isinstance(_score_stats, Unset):
            score_stats = UNSET
        else:
            score_stats = PlayerScoreStats.from_dict(_score_stats)

        last_week_pp = d.pop("lastWeekPp", UNSET)

        last_week_rank = d.pop("lastWeekRank", UNSET)

        last_week_country_rank = d.pop("lastWeekCountryRank", UNSET)

        extension_id = d.pop("extensionId", UNSET)

        mapper_id = d.pop("mapperId", UNSET)

        banned = d.pop("banned", UNSET)

        inactive = d.pop("inactive", UNSET)

        _ban_description = d.pop("banDescription", UNSET)
        ban_description: Union[Unset, Ban]
        if isinstance(_ban_description, Unset):
            ban_description = UNSET
        else:
            ban_description = Ban.from_dict(_ban_description)

        def _parse_external_profile_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_profile_url = _parse_external_profile_url(d.pop("externalProfileUrl", UNSET))

        rich_bio_timeset = d.pop("richBioTimeset", UNSET)

        speedrun_start = d.pop("speedrunStart", UNSET)

        _linked_ids = d.pop("linkedIds", UNSET)
        linked_ids: Union[Unset, LinkResponse]
        if isinstance(_linked_ids, Unset):
            linked_ids = UNSET
        else:
            linked_ids = LinkResponse.from_dict(_linked_ids)

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

        def _parse_pinned_scores(data: object) -> Union[List["ScoreResponseWithMyScore"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                pinned_scores_type_0 = []
                _pinned_scores_type_0 = data
                for pinned_scores_type_0_item_data in _pinned_scores_type_0:
                    pinned_scores_type_0_item = ScoreResponseWithMyScore.from_dict(pinned_scores_type_0_item_data)

                    pinned_scores_type_0.append(pinned_scores_type_0_item)

                return pinned_scores_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ScoreResponseWithMyScore"], None, Unset], data)

        pinned_scores = _parse_pinned_scores(d.pop("pinnedScores", UNSET))

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

        player_response_full = cls(
            id=id,
            name=name,
            platform=platform,
            avatar=avatar,
            country=country,
            alias=alias,
            bot=bot,
            pp=pp,
            rank=rank,
            country_rank=country_rank,
            role=role,
            socials=socials,
            context_extensions=context_extensions,
            patreon_features=patreon_features,
            profile_settings=profile_settings,
            clan_order=clan_order,
            clans=clans,
            acc_pp=acc_pp,
            pass_pp=pass_pp,
            tech_pp=tech_pp,
            score_stats=score_stats,
            last_week_pp=last_week_pp,
            last_week_rank=last_week_rank,
            last_week_country_rank=last_week_country_rank,
            extension_id=extension_id,
            mapper_id=mapper_id,
            banned=banned,
            inactive=inactive,
            ban_description=ban_description,
            external_profile_url=external_profile_url,
            rich_bio_timeset=rich_bio_timeset,
            speedrun_start=speedrun_start,
            linked_ids=linked_ids,
            history=history,
            badges=badges,
            pinned_scores=pinned_scores,
            changes=changes,
        )

        return player_response_full
