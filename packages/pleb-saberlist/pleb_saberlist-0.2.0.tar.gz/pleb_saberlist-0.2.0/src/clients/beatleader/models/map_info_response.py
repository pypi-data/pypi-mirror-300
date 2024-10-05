from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.external_status import ExternalStatus
    from ..models.map_diff_response import MapDiffResponse
    from ..models.mapper_response import MapperResponse


T = TypeVar("T", bound="MapInfoResponse")


@_attrs_define
class MapInfoResponse:
    """
    Attributes:
        id (Union[None, Unset, str]):
        difficulties (Union[List['MapDiffResponse'], None, Unset]):
        hash_ (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        sub_name (Union[None, Unset, str]):
        author (Union[None, Unset, str]):
        mapper (Union[None, Unset, str]):
        mappers (Union[List['MapperResponse'], None, Unset]):
        mapper_id (Union[Unset, int]):
        collaborator_ids (Union[None, Unset, str]):
        cover_image (Union[None, Unset, str]):
        full_cover_image (Union[None, Unset, str]):
        download_url (Union[None, Unset, str]):
        bpm (Union[Unset, float]):
        duration (Union[Unset, float]):
        tags (Union[None, Unset, str]):
        upload_time (Union[Unset, int]):
        external_statuses (Union[List['ExternalStatus'], None, Unset]):
    """

    id: Union[None, Unset, str] = UNSET
    difficulties: Union[List["MapDiffResponse"], None, Unset] = UNSET
    hash_: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    sub_name: Union[None, Unset, str] = UNSET
    author: Union[None, Unset, str] = UNSET
    mapper: Union[None, Unset, str] = UNSET
    mappers: Union[List["MapperResponse"], None, Unset] = UNSET
    mapper_id: Union[Unset, int] = UNSET
    collaborator_ids: Union[None, Unset, str] = UNSET
    cover_image: Union[None, Unset, str] = UNSET
    full_cover_image: Union[None, Unset, str] = UNSET
    download_url: Union[None, Unset, str] = UNSET
    bpm: Union[Unset, float] = UNSET
    duration: Union[Unset, float] = UNSET
    tags: Union[None, Unset, str] = UNSET
    upload_time: Union[Unset, int] = UNSET
    external_statuses: Union[List["ExternalStatus"], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        difficulties: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.difficulties, Unset):
            difficulties = UNSET
        elif isinstance(self.difficulties, list):
            difficulties = []
            for difficulties_type_0_item_data in self.difficulties:
                difficulties_type_0_item = difficulties_type_0_item_data.to_dict()
                difficulties.append(difficulties_type_0_item)

        else:
            difficulties = self.difficulties

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

        mappers: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.mappers, Unset):
            mappers = UNSET
        elif isinstance(self.mappers, list):
            mappers = []
            for mappers_type_0_item_data in self.mappers:
                mappers_type_0_item = mappers_type_0_item_data.to_dict()
                mappers.append(mappers_type_0_item)

        else:
            mappers = self.mappers

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

        full_cover_image: Union[None, Unset, str]
        if isinstance(self.full_cover_image, Unset):
            full_cover_image = UNSET
        else:
            full_cover_image = self.full_cover_image

        download_url: Union[None, Unset, str]
        if isinstance(self.download_url, Unset):
            download_url = UNSET
        else:
            download_url = self.download_url

        bpm = self.bpm

        duration = self.duration

        tags: Union[None, Unset, str]
        if isinstance(self.tags, Unset):
            tags = UNSET
        else:
            tags = self.tags

        upload_time = self.upload_time

        external_statuses: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.external_statuses, Unset):
            external_statuses = UNSET
        elif isinstance(self.external_statuses, list):
            external_statuses = []
            for external_statuses_type_0_item_data in self.external_statuses:
                external_statuses_type_0_item = external_statuses_type_0_item_data.to_dict()
                external_statuses.append(external_statuses_type_0_item)

        else:
            external_statuses = self.external_statuses

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if difficulties is not UNSET:
            field_dict["difficulties"] = difficulties
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
        if mappers is not UNSET:
            field_dict["mappers"] = mappers
        if mapper_id is not UNSET:
            field_dict["mapperId"] = mapper_id
        if collaborator_ids is not UNSET:
            field_dict["collaboratorIds"] = collaborator_ids
        if cover_image is not UNSET:
            field_dict["coverImage"] = cover_image
        if full_cover_image is not UNSET:
            field_dict["fullCoverImage"] = full_cover_image
        if download_url is not UNSET:
            field_dict["downloadUrl"] = download_url
        if bpm is not UNSET:
            field_dict["bpm"] = bpm
        if duration is not UNSET:
            field_dict["duration"] = duration
        if tags is not UNSET:
            field_dict["tags"] = tags
        if upload_time is not UNSET:
            field_dict["uploadTime"] = upload_time
        if external_statuses is not UNSET:
            field_dict["externalStatuses"] = external_statuses

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.external_status import ExternalStatus
        from ..models.map_diff_response import MapDiffResponse
        from ..models.mapper_response import MapperResponse

        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_difficulties(data: object) -> Union[List["MapDiffResponse"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                difficulties_type_0 = []
                _difficulties_type_0 = data
                for difficulties_type_0_item_data in _difficulties_type_0:
                    difficulties_type_0_item = MapDiffResponse.from_dict(difficulties_type_0_item_data)

                    difficulties_type_0.append(difficulties_type_0_item)

                return difficulties_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["MapDiffResponse"], None, Unset], data)

        difficulties = _parse_difficulties(d.pop("difficulties", UNSET))

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

        def _parse_mappers(data: object) -> Union[List["MapperResponse"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                mappers_type_0 = []
                _mappers_type_0 = data
                for mappers_type_0_item_data in _mappers_type_0:
                    mappers_type_0_item = MapperResponse.from_dict(mappers_type_0_item_data)

                    mappers_type_0.append(mappers_type_0_item)

                return mappers_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["MapperResponse"], None, Unset], data)

        mappers = _parse_mappers(d.pop("mappers", UNSET))

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

        def _parse_full_cover_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        full_cover_image = _parse_full_cover_image(d.pop("fullCoverImage", UNSET))

        def _parse_download_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        download_url = _parse_download_url(d.pop("downloadUrl", UNSET))

        bpm = d.pop("bpm", UNSET)

        duration = d.pop("duration", UNSET)

        def _parse_tags(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        upload_time = d.pop("uploadTime", UNSET)

        def _parse_external_statuses(data: object) -> Union[List["ExternalStatus"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                external_statuses_type_0 = []
                _external_statuses_type_0 = data
                for external_statuses_type_0_item_data in _external_statuses_type_0:
                    external_statuses_type_0_item = ExternalStatus.from_dict(external_statuses_type_0_item_data)

                    external_statuses_type_0.append(external_statuses_type_0_item)

                return external_statuses_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ExternalStatus"], None, Unset], data)

        external_statuses = _parse_external_statuses(d.pop("externalStatuses", UNSET))

        map_info_response = cls(
            id=id,
            difficulties=difficulties,
            hash_=hash_,
            name=name,
            sub_name=sub_name,
            author=author,
            mapper=mapper,
            mappers=mappers,
            mapper_id=mapper_id,
            collaborator_ids=collaborator_ids,
            cover_image=cover_image,
            full_cover_image=full_cover_image,
            download_url=download_url,
            bpm=bpm,
            duration=duration,
            tags=tags,
            upload_time=upload_time,
            external_statuses=external_statuses,
        )

        return map_info_response
