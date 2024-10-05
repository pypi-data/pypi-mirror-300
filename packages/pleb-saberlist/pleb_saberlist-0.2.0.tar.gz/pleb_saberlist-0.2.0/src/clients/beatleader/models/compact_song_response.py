from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CompactSongResponse")


@_attrs_define
class CompactSongResponse:
    """
    Attributes:
        id (Union[None, Unset, str]):
        hash_ (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        sub_name (Union[None, Unset, str]):
        author (Union[None, Unset, str]):
        mapper (Union[None, Unset, str]):
        mapper_id (Union[Unset, int]):
        collaborator_ids (Union[None, Unset, str]):
        cover_image (Union[None, Unset, str]):
        bpm (Union[Unset, float]):
        duration (Union[Unset, float]):
        full_cover_image (Union[None, Unset, str]):
    """

    id: Union[None, Unset, str] = UNSET
    hash_: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    sub_name: Union[None, Unset, str] = UNSET
    author: Union[None, Unset, str] = UNSET
    mapper: Union[None, Unset, str] = UNSET
    mapper_id: Union[Unset, int] = UNSET
    collaborator_ids: Union[None, Unset, str] = UNSET
    cover_image: Union[None, Unset, str] = UNSET
    bpm: Union[Unset, float] = UNSET
    duration: Union[Unset, float] = UNSET
    full_cover_image: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        hash_: Union[None, Unset, str]
        if isinstance(self.hash_, Unset):
            hash_ = UNSET
        else:
            hash_ = self.hash_

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        sub_name: Union[None, Unset, str]
        if isinstance(self.sub_name, Unset):
            sub_name = UNSET
        else:
            sub_name = self.sub_name

        author: Union[None, Unset, str]
        if isinstance(self.author, Unset):
            author = UNSET
        else:
            author = self.author

        mapper: Union[None, Unset, str]
        if isinstance(self.mapper, Unset):
            mapper = UNSET
        else:
            mapper = self.mapper

        mapper_id = self.mapper_id

        collaborator_ids: Union[None, Unset, str]
        if isinstance(self.collaborator_ids, Unset):
            collaborator_ids = UNSET
        else:
            collaborator_ids = self.collaborator_ids

        cover_image: Union[None, Unset, str]
        if isinstance(self.cover_image, Unset):
            cover_image = UNSET
        else:
            cover_image = self.cover_image

        bpm = self.bpm

        duration = self.duration

        full_cover_image: Union[None, Unset, str]
        if isinstance(self.full_cover_image, Unset):
            full_cover_image = UNSET
        else:
            full_cover_image = self.full_cover_image

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if hash_ is not UNSET:
            field_dict["hash"] = hash_
        if name is not UNSET:
            field_dict["name"] = name
        if sub_name is not UNSET:
            field_dict["subName"] = sub_name
        if author is not UNSET:
            field_dict["author"] = author
        if mapper is not UNSET:
            field_dict["mapper"] = mapper
        if mapper_id is not UNSET:
            field_dict["mapperId"] = mapper_id
        if collaborator_ids is not UNSET:
            field_dict["collaboratorIds"] = collaborator_ids
        if cover_image is not UNSET:
            field_dict["coverImage"] = cover_image
        if bpm is not UNSET:
            field_dict["bpm"] = bpm
        if duration is not UNSET:
            field_dict["duration"] = duration
        if full_cover_image is not UNSET:
            field_dict["fullCoverImage"] = full_cover_image

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_hash_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        hash_ = _parse_hash_(d.pop("hash", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_sub_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sub_name = _parse_sub_name(d.pop("subName", UNSET))

        def _parse_author(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        author = _parse_author(d.pop("author", UNSET))

        def _parse_mapper(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mapper = _parse_mapper(d.pop("mapper", UNSET))

        mapper_id = d.pop("mapperId", UNSET)

        def _parse_collaborator_ids(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        collaborator_ids = _parse_collaborator_ids(d.pop("collaboratorIds", UNSET))

        def _parse_cover_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cover_image = _parse_cover_image(d.pop("coverImage", UNSET))

        bpm = d.pop("bpm", UNSET)

        duration = d.pop("duration", UNSET)

        def _parse_full_cover_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        full_cover_image = _parse_full_cover_image(d.pop("fullCoverImage", UNSET))

        compact_song_response = cls(
            id=id,
            hash_=hash_,
            name=name,
            sub_name=sub_name,
            author=author,
            mapper=mapper,
            mapper_id=mapper_id,
            collaborator_ids=collaborator_ids,
            cover_image=cover_image,
            bpm=bpm,
            duration=duration,
            full_cover_image=full_cover_image,
        )

        return compact_song_response
