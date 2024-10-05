from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.clan_response import ClanResponse
    from ..models.patreon_features import PatreonFeatures
    from ..models.player_context_extension import PlayerContextExtension
    from ..models.player_social import PlayerSocial
    from ..models.profile_settings import ProfileSettings


T = TypeVar("T", bound="PlayerResponse")


@_attrs_define
class PlayerResponse:
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.clan_response import ClanResponse
        from ..models.patreon_features import PatreonFeatures
        from ..models.player_context_extension import PlayerContextExtension
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

        player_response = cls(
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
        )

        return player_response
