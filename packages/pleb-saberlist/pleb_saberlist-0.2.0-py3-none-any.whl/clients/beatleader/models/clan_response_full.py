from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.featured_playlist_response import FeaturedPlaylistResponse


T = TypeVar("T", bound="ClanResponseFull")


@_attrs_define
class ClanResponseFull:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[None, Unset, str]):
        color (Union[None, Unset, str]):
        icon (Union[None, Unset, str]):
        tag (Union[None, Unset, str]):
        leader_id (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        bio (Union[None, Unset, str]):
        rich_bio_timeset (Union[Unset, int]):
        discord_invite (Union[None, Unset, str]):
        players_count (Union[Unset, int]):
        pp (Union[Unset, float]):
        rank (Union[Unset, int]):
        average_rank (Union[Unset, float]):
        average_accuracy (Union[Unset, float]):
        ranked_pool_percent_captured (Union[Unset, float]):
        capture_leaderboards_count (Union[Unset, int]):
        player_changes_callback (Union[None, Unset, str]):
        clan_ranking_discord_hook (Union[None, Unset, str]):
        featured_playlists (Union[List['FeaturedPlaylistResponse'], None, Unset]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[None, Unset, str] = UNSET
    color: Union[None, Unset, str] = UNSET
    icon: Union[None, Unset, str] = UNSET
    tag: Union[None, Unset, str] = UNSET
    leader_id: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    bio: Union[None, Unset, str] = UNSET
    rich_bio_timeset: Union[Unset, int] = UNSET
    discord_invite: Union[None, Unset, str] = UNSET
    players_count: Union[Unset, int] = UNSET
    pp: Union[Unset, float] = UNSET
    rank: Union[Unset, int] = UNSET
    average_rank: Union[Unset, float] = UNSET
    average_accuracy: Union[Unset, float] = UNSET
    ranked_pool_percent_captured: Union[Unset, float] = UNSET
    capture_leaderboards_count: Union[Unset, int] = UNSET
    player_changes_callback: Union[None, Unset, str] = UNSET
    clan_ranking_discord_hook: Union[None, Unset, str] = UNSET
    featured_playlists: Union[List["FeaturedPlaylistResponse"], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        color: Union[None, Unset, str]
        if isinstance(self.color, Unset):
            color = UNSET
        else:
            color = self.color

        icon: Union[None, Unset, str]
        if isinstance(self.icon, Unset):
            icon = UNSET
        else:
            icon = self.icon

        tag: Union[None, Unset, str]
        if isinstance(self.tag, Unset):
            tag = UNSET
        else:
            tag = self.tag

        leader_id: Union[None, Unset, str]
        if isinstance(self.leader_id, Unset):
            leader_id = UNSET
        else:
            leader_id = self.leader_id

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        bio: Union[None, Unset, str]
        if isinstance(self.bio, Unset):
            bio = UNSET
        else:
            bio = self.bio

        rich_bio_timeset = self.rich_bio_timeset

        discord_invite: Union[None, Unset, str]
        if isinstance(self.discord_invite, Unset):
            discord_invite = UNSET
        else:
            discord_invite = self.discord_invite

        players_count = self.players_count

        pp = self.pp

        rank = self.rank

        average_rank = self.average_rank

        average_accuracy = self.average_accuracy

        ranked_pool_percent_captured = self.ranked_pool_percent_captured

        capture_leaderboards_count = self.capture_leaderboards_count

        player_changes_callback: Union[None, Unset, str]
        if isinstance(self.player_changes_callback, Unset):
            player_changes_callback = UNSET
        else:
            player_changes_callback = self.player_changes_callback

        clan_ranking_discord_hook: Union[None, Unset, str]
        if isinstance(self.clan_ranking_discord_hook, Unset):
            clan_ranking_discord_hook = UNSET
        else:
            clan_ranking_discord_hook = self.clan_ranking_discord_hook

        featured_playlists: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.featured_playlists, Unset):
            featured_playlists = UNSET
        elif isinstance(self.featured_playlists, list):
            featured_playlists = []
            for featured_playlists_type_0_item_data in self.featured_playlists:
                featured_playlists_type_0_item = featured_playlists_type_0_item_data.to_dict()
                featured_playlists.append(featured_playlists_type_0_item)

        else:
            featured_playlists = self.featured_playlists

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if color is not UNSET:
            field_dict["color"] = color
        if icon is not UNSET:
            field_dict["icon"] = icon
        if tag is not UNSET:
            field_dict["tag"] = tag
        if leader_id is not UNSET:
            field_dict["leaderID"] = leader_id
        if description is not UNSET:
            field_dict["description"] = description
        if bio is not UNSET:
            field_dict["bio"] = bio
        if rich_bio_timeset is not UNSET:
            field_dict["richBioTimeset"] = rich_bio_timeset
        if discord_invite is not UNSET:
            field_dict["discordInvite"] = discord_invite
        if players_count is not UNSET:
            field_dict["playersCount"] = players_count
        if pp is not UNSET:
            field_dict["pp"] = pp
        if rank is not UNSET:
            field_dict["rank"] = rank
        if average_rank is not UNSET:
            field_dict["averageRank"] = average_rank
        if average_accuracy is not UNSET:
            field_dict["averageAccuracy"] = average_accuracy
        if ranked_pool_percent_captured is not UNSET:
            field_dict["rankedPoolPercentCaptured"] = ranked_pool_percent_captured
        if capture_leaderboards_count is not UNSET:
            field_dict["captureLeaderboardsCount"] = capture_leaderboards_count
        if player_changes_callback is not UNSET:
            field_dict["playerChangesCallback"] = player_changes_callback
        if clan_ranking_discord_hook is not UNSET:
            field_dict["clanRankingDiscordHook"] = clan_ranking_discord_hook
        if featured_playlists is not UNSET:
            field_dict["featuredPlaylists"] = featured_playlists

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.featured_playlist_response import FeaturedPlaylistResponse

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        color = _parse_color(d.pop("color", UNSET))

        def _parse_icon(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        icon = _parse_icon(d.pop("icon", UNSET))

        def _parse_tag(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tag = _parse_tag(d.pop("tag", UNSET))

        def _parse_leader_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        leader_id = _parse_leader_id(d.pop("leaderID", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_bio(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bio = _parse_bio(d.pop("bio", UNSET))

        rich_bio_timeset = d.pop("richBioTimeset", UNSET)

        def _parse_discord_invite(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        discord_invite = _parse_discord_invite(d.pop("discordInvite", UNSET))

        players_count = d.pop("playersCount", UNSET)

        pp = d.pop("pp", UNSET)

        rank = d.pop("rank", UNSET)

        average_rank = d.pop("averageRank", UNSET)

        average_accuracy = d.pop("averageAccuracy", UNSET)

        ranked_pool_percent_captured = d.pop("rankedPoolPercentCaptured", UNSET)

        capture_leaderboards_count = d.pop("captureLeaderboardsCount", UNSET)

        def _parse_player_changes_callback(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_changes_callback = _parse_player_changes_callback(d.pop("playerChangesCallback", UNSET))

        def _parse_clan_ranking_discord_hook(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        clan_ranking_discord_hook = _parse_clan_ranking_discord_hook(d.pop("clanRankingDiscordHook", UNSET))

        def _parse_featured_playlists(data: object) -> Union[List["FeaturedPlaylistResponse"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                featured_playlists_type_0 = []
                _featured_playlists_type_0 = data
                for featured_playlists_type_0_item_data in _featured_playlists_type_0:
                    featured_playlists_type_0_item = FeaturedPlaylistResponse.from_dict(
                        featured_playlists_type_0_item_data
                    )

                    featured_playlists_type_0.append(featured_playlists_type_0_item)

                return featured_playlists_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["FeaturedPlaylistResponse"], None, Unset], data)

        featured_playlists = _parse_featured_playlists(d.pop("featuredPlaylists", UNSET))

        clan_response_full = cls(
            id=id,
            name=name,
            color=color,
            icon=icon,
            tag=tag,
            leader_id=leader_id,
            description=description,
            bio=bio,
            rich_bio_timeset=rich_bio_timeset,
            discord_invite=discord_invite,
            players_count=players_count,
            pp=pp,
            rank=rank,
            average_rank=average_rank,
            average_accuracy=average_accuracy,
            ranked_pool_percent_captured=ranked_pool_percent_captured,
            capture_leaderboards_count=capture_leaderboards_count,
            player_changes_callback=player_changes_callback,
            clan_ranking_discord_hook=clan_ranking_discord_hook,
            featured_playlists=featured_playlists,
        )

        return clan_response_full
