import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.playlist_full_type import PlaylistFullType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.playlist_stats import PlaylistStats
    from ..models.user_detail import UserDetail


T = TypeVar("T", bound="PlaylistFull")


@_attrs_define
class PlaylistFull:
    """
    Attributes:
        config (Union[Unset, Any]):
        created_at (Union[Unset, datetime.datetime]):
        curated_at (Union[Unset, datetime.datetime]):
        curator (Union[Unset, UserDetail]):
        deleted_at (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        download_url (Union[Unset, str]):
        name (Union[Unset, str]):
        owner (Union[Unset, UserDetail]):
        playlist_id (Union[Unset, int]):
        playlist_image (Union[Unset, str]):
        playlist_image_512 (Union[Unset, str]):
        songs_changed_at (Union[Unset, datetime.datetime]):
        stats (Union[Unset, PlaylistStats]):
        type (Union[Unset, PlaylistFullType]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    config: Union[Unset, Any] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    curated_at: Union[Unset, datetime.datetime] = UNSET
    curator: Union[Unset, "UserDetail"] = UNSET
    deleted_at: Union[Unset, datetime.datetime] = UNSET
    description: Union[Unset, str] = UNSET
    download_url: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    owner: Union[Unset, "UserDetail"] = UNSET
    playlist_id: Union[Unset, int] = UNSET
    playlist_image: Union[Unset, str] = UNSET
    playlist_image_512: Union[Unset, str] = UNSET
    songs_changed_at: Union[Unset, datetime.datetime] = UNSET
    stats: Union[Unset, "PlaylistStats"] = UNSET
    type: Union[Unset, PlaylistFullType] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config = self.config

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        curated_at: Union[Unset, str] = UNSET
        if not isinstance(self.curated_at, Unset):
            curated_at = self.curated_at.isoformat()

        curator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.curator, Unset):
            curator = self.curator.to_dict()

        deleted_at: Union[Unset, str] = UNSET
        if not isinstance(self.deleted_at, Unset):
            deleted_at = self.deleted_at.isoformat()

        description = self.description

        download_url = self.download_url

        name = self.name

        owner: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.owner, Unset):
            owner = self.owner.to_dict()

        playlist_id = self.playlist_id

        playlist_image = self.playlist_image

        playlist_image_512 = self.playlist_image_512

        songs_changed_at: Union[Unset, str] = UNSET
        if not isinstance(self.songs_changed_at, Unset):
            songs_changed_at = self.songs_changed_at.isoformat()

        stats: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stats, Unset):
            stats = self.stats.to_dict()

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if curated_at is not UNSET:
            field_dict["curatedAt"] = curated_at
        if curator is not UNSET:
            field_dict["curator"] = curator
        if deleted_at is not UNSET:
            field_dict["deletedAt"] = deleted_at
        if description is not UNSET:
            field_dict["description"] = description
        if download_url is not UNSET:
            field_dict["downloadURL"] = download_url
        if name is not UNSET:
            field_dict["name"] = name
        if owner is not UNSET:
            field_dict["owner"] = owner
        if playlist_id is not UNSET:
            field_dict["playlistId"] = playlist_id
        if playlist_image is not UNSET:
            field_dict["playlistImage"] = playlist_image
        if playlist_image_512 is not UNSET:
            field_dict["playlistImage512"] = playlist_image_512
        if songs_changed_at is not UNSET:
            field_dict["songsChangedAt"] = songs_changed_at
        if stats is not UNSET:
            field_dict["stats"] = stats
        if type is not UNSET:
            field_dict["type"] = type
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.playlist_stats import PlaylistStats
        from ..models.user_detail import UserDetail

        d = src_dict.copy()
        config = d.pop("config", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _curated_at = d.pop("curatedAt", UNSET)
        curated_at: Union[Unset, datetime.datetime]
        if isinstance(_curated_at, Unset):
            curated_at = UNSET
        else:
            curated_at = isoparse(_curated_at)

        _curator = d.pop("curator", UNSET)
        curator: Union[Unset, UserDetail]
        if isinstance(_curator, Unset):
            curator = UNSET
        else:
            curator = UserDetail.from_dict(_curator)

        _deleted_at = d.pop("deletedAt", UNSET)
        deleted_at: Union[Unset, datetime.datetime]
        if isinstance(_deleted_at, Unset):
            deleted_at = UNSET
        else:
            deleted_at = isoparse(_deleted_at)

        description = d.pop("description", UNSET)

        download_url = d.pop("downloadURL", UNSET)

        name = d.pop("name", UNSET)

        _owner = d.pop("owner", UNSET)
        owner: Union[Unset, UserDetail]
        if isinstance(_owner, Unset):
            owner = UNSET
        else:
            owner = UserDetail.from_dict(_owner)

        playlist_id = d.pop("playlistId", UNSET)

        playlist_image = d.pop("playlistImage", UNSET)

        playlist_image_512 = d.pop("playlistImage512", UNSET)

        _songs_changed_at = d.pop("songsChangedAt", UNSET)
        songs_changed_at: Union[Unset, datetime.datetime]
        if isinstance(_songs_changed_at, Unset):
            songs_changed_at = UNSET
        else:
            songs_changed_at = isoparse(_songs_changed_at)

        _stats = d.pop("stats", UNSET)
        stats: Union[Unset, PlaylistStats]
        if isinstance(_stats, Unset):
            stats = UNSET
        else:
            stats = PlaylistStats.from_dict(_stats)

        _type = d.pop("type", UNSET)
        type: Union[Unset, PlaylistFullType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = PlaylistFullType(_type)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        playlist_full = cls(
            config=config,
            created_at=created_at,
            curated_at=curated_at,
            curator=curator,
            deleted_at=deleted_at,
            description=description,
            download_url=download_url,
            name=name,
            owner=owner,
            playlist_id=playlist_id,
            playlist_image=playlist_image,
            playlist_image_512=playlist_image_512,
            songs_changed_at=songs_changed_at,
            stats=stats,
            type=type,
            updated_at=updated_at,
        )

        playlist_full.additional_properties = d
        return playlist_full

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
