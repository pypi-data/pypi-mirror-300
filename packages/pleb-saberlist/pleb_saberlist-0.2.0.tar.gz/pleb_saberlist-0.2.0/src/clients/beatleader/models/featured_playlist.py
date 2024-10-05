from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="FeaturedPlaylist")


@_attrs_define
class FeaturedPlaylist:
    """
    Attributes:
        id (Union[Unset, int]):
        playlist_link (Union[None, Unset, str]):
        cover (Union[None, Unset, str]):
        title (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        owner (Union[None, Unset, str]):
        owner_cover (Union[None, Unset, str]):
        owner_link (Union[None, Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    playlist_link: Union[None, Unset, str] = UNSET
    cover: Union[None, Unset, str] = UNSET
    title: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    owner: Union[None, Unset, str] = UNSET
    owner_cover: Union[None, Unset, str] = UNSET
    owner_link: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        playlist_link: Union[None, Unset, str]
        if isinstance(self.playlist_link, Unset):
            playlist_link = UNSET
        else:
            playlist_link = self.playlist_link

        cover: Union[None, Unset, str]
        if isinstance(self.cover, Unset):
            cover = UNSET
        else:
            cover = self.cover

        title: Union[None, Unset, str]
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        owner: Union[None, Unset, str]
        if isinstance(self.owner, Unset):
            owner = UNSET
        else:
            owner = self.owner

        owner_cover: Union[None, Unset, str]
        if isinstance(self.owner_cover, Unset):
            owner_cover = UNSET
        else:
            owner_cover = self.owner_cover

        owner_link: Union[None, Unset, str]
        if isinstance(self.owner_link, Unset):
            owner_link = UNSET
        else:
            owner_link = self.owner_link

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if playlist_link is not UNSET:
            field_dict["playlistLink"] = playlist_link
        if cover is not UNSET:
            field_dict["cover"] = cover
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if owner is not UNSET:
            field_dict["owner"] = owner
        if owner_cover is not UNSET:
            field_dict["ownerCover"] = owner_cover
        if owner_link is not UNSET:
            field_dict["ownerLink"] = owner_link

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_playlist_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        playlist_link = _parse_playlist_link(d.pop("playlistLink", UNSET))

        def _parse_cover(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cover = _parse_cover(d.pop("cover", UNSET))

        def _parse_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_owner(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        owner = _parse_owner(d.pop("owner", UNSET))

        def _parse_owner_cover(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        owner_cover = _parse_owner_cover(d.pop("ownerCover", UNSET))

        def _parse_owner_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        owner_link = _parse_owner_link(d.pop("ownerLink", UNSET))

        featured_playlist = cls(
            id=id,
            playlist_link=playlist_link,
            cover=cover,
            title=title,
            description=description,
            owner=owner,
            owner_cover=owner_cover,
            owner_link=owner_link,
        )

        return featured_playlist
