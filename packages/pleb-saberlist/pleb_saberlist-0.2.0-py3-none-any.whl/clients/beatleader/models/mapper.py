from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.player import Player
    from ..models.song import Song


T = TypeVar("T", bound="Mapper")


@_attrs_define
class Mapper:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[None, Unset, str]):
        avatar (Union[None, Unset, str]):
        curator (Union[None, Unset, bool]):
        verified_mapper (Union[Unset, bool]):
        playlist_url (Union[None, Unset, str]):
        songs (Union[List['Song'], None, Unset]):
        player (Union[Unset, Player]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[None, Unset, str] = UNSET
    avatar: Union[None, Unset, str] = UNSET
    curator: Union[None, Unset, bool] = UNSET
    verified_mapper: Union[Unset, bool] = UNSET
    playlist_url: Union[None, Unset, str] = UNSET
    songs: Union[List["Song"], None, Unset] = UNSET
    player: Union[Unset, "Player"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        avatar: Union[None, Unset, str]
        if isinstance(self.avatar, Unset):
            avatar = UNSET
        else:
            avatar = self.avatar

        curator: Union[None, Unset, bool]
        if isinstance(self.curator, Unset):
            curator = UNSET
        else:
            curator = self.curator

        verified_mapper = self.verified_mapper

        playlist_url: Union[None, Unset, str]
        if isinstance(self.playlist_url, Unset):
            playlist_url = UNSET
        else:
            playlist_url = self.playlist_url

        songs: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.songs, Unset):
            songs = UNSET
        elif isinstance(self.songs, list):
            songs = []
            for songs_type_0_item_data in self.songs:
                songs_type_0_item = songs_type_0_item_data.to_dict()
                songs.append(songs_type_0_item)

        else:
            songs = self.songs

        player: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.player, Unset):
            player = self.player.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if avatar is not UNSET:
            field_dict["avatar"] = avatar
        if curator is not UNSET:
            field_dict["curator"] = curator
        if verified_mapper is not UNSET:
            field_dict["verifiedMapper"] = verified_mapper
        if playlist_url is not UNSET:
            field_dict["playlistUrl"] = playlist_url
        if songs is not UNSET:
            field_dict["songs"] = songs
        if player is not UNSET:
            field_dict["player"] = player

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.player import Player
        from ..models.song import Song

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_avatar(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        avatar = _parse_avatar(d.pop("avatar", UNSET))

        def _parse_curator(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        curator = _parse_curator(d.pop("curator", UNSET))

        verified_mapper = d.pop("verifiedMapper", UNSET)

        def _parse_playlist_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        playlist_url = _parse_playlist_url(d.pop("playlistUrl", UNSET))

        def _parse_songs(data: object) -> Union[List["Song"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                songs_type_0 = []
                _songs_type_0 = data
                for songs_type_0_item_data in _songs_type_0:
                    songs_type_0_item = Song.from_dict(songs_type_0_item_data)

                    songs_type_0.append(songs_type_0_item)

                return songs_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["Song"], None, Unset], data)

        songs = _parse_songs(d.pop("songs", UNSET))

        _player = d.pop("player", UNSET)
        player: Union[Unset, Player]
        if isinstance(_player, Unset):
            player = UNSET
        else:
            player = Player.from_dict(_player)

        mapper = cls(
            id=id,
            name=name,
            avatar=avatar,
            curator=curator,
            verified_mapper=verified_mapper,
            playlist_url=playlist_url,
            songs=songs,
            player=player,
        )

        return mapper
