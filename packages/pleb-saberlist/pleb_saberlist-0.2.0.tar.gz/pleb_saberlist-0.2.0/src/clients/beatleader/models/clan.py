from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.featured_playlist import FeaturedPlaylist
    from ..models.leaderboard import Leaderboard


T = TypeVar("T", bound="Clan")


@_attrs_define
class Clan:
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
        players_count (Union[Unset, int]):
        pp (Union[Unset, float]):
        rank (Union[Unset, int]):
        average_rank (Union[Unset, float]):
        average_accuracy (Union[Unset, float]):
        featured_playlists (Union[List['FeaturedPlaylist'], None, Unset]):
        ranked_pool_percent_captured (Union[Unset, float]):
        capture_leaderboards_count (Union[Unset, int]):
        captured_leaderboards (Union[List['Leaderboard'], None, Unset]):
        global_map_x (Union[Unset, float]):
        global_map_y (Union[Unset, float]):
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
    players_count: Union[Unset, int] = UNSET
    pp: Union[Unset, float] = UNSET
    rank: Union[Unset, int] = UNSET
    average_rank: Union[Unset, float] = UNSET
    average_accuracy: Union[Unset, float] = UNSET
    featured_playlists: Union[List["FeaturedPlaylist"], None, Unset] = UNSET
    ranked_pool_percent_captured: Union[Unset, float] = UNSET
    capture_leaderboards_count: Union[Unset, int] = UNSET
    captured_leaderboards: Union[List["Leaderboard"], None, Unset] = UNSET
    global_map_x: Union[Unset, float] = UNSET
    global_map_y: Union[Unset, float] = UNSET

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

        players_count = self.players_count

        pp = self.pp

        rank = self.rank

        average_rank = self.average_rank

        average_accuracy = self.average_accuracy

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

        ranked_pool_percent_captured = self.ranked_pool_percent_captured

        capture_leaderboards_count = self.capture_leaderboards_count

        captured_leaderboards: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.captured_leaderboards, Unset):
            captured_leaderboards = UNSET
        elif isinstance(self.captured_leaderboards, list):
            captured_leaderboards = []
            for captured_leaderboards_type_0_item_data in self.captured_leaderboards:
                captured_leaderboards_type_0_item = captured_leaderboards_type_0_item_data.to_dict()
                captured_leaderboards.append(captured_leaderboards_type_0_item)

        else:
            captured_leaderboards = self.captured_leaderboards

        global_map_x = self.global_map_x

        global_map_y = self.global_map_y

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
        if featured_playlists is not UNSET:
            field_dict["featuredPlaylists"] = featured_playlists
        if ranked_pool_percent_captured is not UNSET:
            field_dict["rankedPoolPercentCaptured"] = ranked_pool_percent_captured
        if capture_leaderboards_count is not UNSET:
            field_dict["captureLeaderboardsCount"] = capture_leaderboards_count
        if captured_leaderboards is not UNSET:
            field_dict["capturedLeaderboards"] = captured_leaderboards
        if global_map_x is not UNSET:
            field_dict["globalMapX"] = global_map_x
        if global_map_y is not UNSET:
            field_dict["globalMapY"] = global_map_y

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.featured_playlist import FeaturedPlaylist
        from ..models.leaderboard import Leaderboard

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

        players_count = d.pop("playersCount", UNSET)

        pp = d.pop("pp", UNSET)

        rank = d.pop("rank", UNSET)

        average_rank = d.pop("averageRank", UNSET)

        average_accuracy = d.pop("averageAccuracy", UNSET)

        def _parse_featured_playlists(data: object) -> Union[List["FeaturedPlaylist"], None, Unset]:
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
                    featured_playlists_type_0_item = FeaturedPlaylist.from_dict(featured_playlists_type_0_item_data)

                    featured_playlists_type_0.append(featured_playlists_type_0_item)

                return featured_playlists_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["FeaturedPlaylist"], None, Unset], data)

        featured_playlists = _parse_featured_playlists(d.pop("featuredPlaylists", UNSET))

        ranked_pool_percent_captured = d.pop("rankedPoolPercentCaptured", UNSET)

        capture_leaderboards_count = d.pop("captureLeaderboardsCount", UNSET)

        def _parse_captured_leaderboards(data: object) -> Union[List["Leaderboard"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                captured_leaderboards_type_0 = []
                _captured_leaderboards_type_0 = data
                for captured_leaderboards_type_0_item_data in _captured_leaderboards_type_0:
                    captured_leaderboards_type_0_item = Leaderboard.from_dict(captured_leaderboards_type_0_item_data)

                    captured_leaderboards_type_0.append(captured_leaderboards_type_0_item)

                return captured_leaderboards_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["Leaderboard"], None, Unset], data)

        captured_leaderboards = _parse_captured_leaderboards(d.pop("capturedLeaderboards", UNSET))

        global_map_x = d.pop("globalMapX", UNSET)

        global_map_y = d.pop("globalMapY", UNSET)

        clan = cls(
            id=id,
            name=name,
            color=color,
            icon=icon,
            tag=tag,
            leader_id=leader_id,
            description=description,
            bio=bio,
            rich_bio_timeset=rich_bio_timeset,
            players_count=players_count,
            pp=pp,
            rank=rank,
            average_rank=average_rank,
            average_accuracy=average_accuracy,
            featured_playlists=featured_playlists,
            ranked_pool_percent_captured=ranked_pool_percent_captured,
            capture_leaderboards_count=capture_leaderboards_count,
            captured_leaderboards=captured_leaderboards,
            global_map_x=global_map_x,
            global_map_y=global_map_y,
        )

        return clan
