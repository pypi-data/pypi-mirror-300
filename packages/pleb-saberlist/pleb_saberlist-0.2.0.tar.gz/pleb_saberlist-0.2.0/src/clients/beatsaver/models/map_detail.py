import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.map_detail_declared_ai import MapDetailDeclaredAi
from ..models.map_detail_tags_item import MapDetailTagsItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.map_detail_metadata import MapDetailMetadata
    from ..models.map_stats import MapStats
    from ..models.map_version import MapVersion
    from ..models.user_detail import UserDetail


T = TypeVar("T", bound="MapDetail")


@_attrs_define
class MapDetail:
    """
    Attributes:
        automapper (Union[Unset, bool]):
        bl_qualified (Union[Unset, bool]):
        bl_ranked (Union[Unset, bool]):
        bookmarked (Union[Unset, bool]):
        collaborators (Union[Unset, List['UserDetail']]):
        created_at (Union[Unset, datetime.datetime]):
        curated_at (Union[Unset, datetime.datetime]):
        curator (Union[Unset, UserDetail]):
        declared_ai (Union[Unset, MapDetailDeclaredAi]):
        deleted_at (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        id (Union[Unset, str]):
        last_published_at (Union[Unset, datetime.datetime]):
        metadata (Union[Unset, MapDetailMetadata]):
        name (Union[Unset, str]):
        qualified (Union[Unset, bool]):
        ranked (Union[Unset, bool]):
        stats (Union[Unset, MapStats]):
        tags (Union[Unset, List[MapDetailTagsItem]]):
        updated_at (Union[Unset, datetime.datetime]):
        uploaded (Union[Unset, datetime.datetime]):
        uploader (Union[Unset, UserDetail]):
        versions (Union[Unset, List['MapVersion']]):
    """

    automapper: Union[Unset, bool] = UNSET
    bl_qualified: Union[Unset, bool] = UNSET
    bl_ranked: Union[Unset, bool] = UNSET
    bookmarked: Union[Unset, bool] = UNSET
    collaborators: Union[Unset, List["UserDetail"]] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    curated_at: Union[Unset, datetime.datetime] = UNSET
    curator: Union[Unset, "UserDetail"] = UNSET
    declared_ai: Union[Unset, MapDetailDeclaredAi] = UNSET
    deleted_at: Union[Unset, datetime.datetime] = UNSET
    description: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    last_published_at: Union[Unset, datetime.datetime] = UNSET
    metadata: Union[Unset, "MapDetailMetadata"] = UNSET
    name: Union[Unset, str] = UNSET
    qualified: Union[Unset, bool] = UNSET
    ranked: Union[Unset, bool] = UNSET
    stats: Union[Unset, "MapStats"] = UNSET
    tags: Union[Unset, List[MapDetailTagsItem]] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    uploaded: Union[Unset, datetime.datetime] = UNSET
    uploader: Union[Unset, "UserDetail"] = UNSET
    versions: Union[Unset, List["MapVersion"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        automapper = self.automapper

        bl_qualified = self.bl_qualified

        bl_ranked = self.bl_ranked

        bookmarked = self.bookmarked

        collaborators: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.collaborators, Unset):
            collaborators = []
            for collaborators_item_data in self.collaborators:
                collaborators_item = collaborators_item_data.to_dict()
                collaborators.append(collaborators_item)

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        curated_at: Union[Unset, str] = UNSET
        if not isinstance(self.curated_at, Unset):
            curated_at = self.curated_at.isoformat()

        curator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.curator, Unset):
            curator = self.curator.to_dict()

        declared_ai: Union[Unset, str] = UNSET
        if not isinstance(self.declared_ai, Unset):
            declared_ai = self.declared_ai.value

        deleted_at: Union[Unset, str] = UNSET
        if not isinstance(self.deleted_at, Unset):
            deleted_at = self.deleted_at.isoformat()

        description = self.description

        id = self.id

        last_published_at: Union[Unset, str] = UNSET
        if not isinstance(self.last_published_at, Unset):
            last_published_at = self.last_published_at.isoformat()

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        name = self.name

        qualified = self.qualified

        ranked = self.ranked

        stats: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stats, Unset):
            stats = self.stats.to_dict()

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.value
                tags.append(tags_item)

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        uploaded: Union[Unset, str] = UNSET
        if not isinstance(self.uploaded, Unset):
            uploaded = self.uploaded.isoformat()

        uploader: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.uploader, Unset):
            uploader = self.uploader.to_dict()

        versions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.versions, Unset):
            versions = []
            for versions_item_data in self.versions:
                versions_item = versions_item_data.to_dict()
                versions.append(versions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if automapper is not UNSET:
            field_dict["automapper"] = automapper
        if bl_qualified is not UNSET:
            field_dict["blQualified"] = bl_qualified
        if bl_ranked is not UNSET:
            field_dict["blRanked"] = bl_ranked
        if bookmarked is not UNSET:
            field_dict["bookmarked"] = bookmarked
        if collaborators is not UNSET:
            field_dict["collaborators"] = collaborators
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if curated_at is not UNSET:
            field_dict["curatedAt"] = curated_at
        if curator is not UNSET:
            field_dict["curator"] = curator
        if declared_ai is not UNSET:
            field_dict["declaredAi"] = declared_ai
        if deleted_at is not UNSET:
            field_dict["deletedAt"] = deleted_at
        if description is not UNSET:
            field_dict["description"] = description
        if id is not UNSET:
            field_dict["id"] = id
        if last_published_at is not UNSET:
            field_dict["lastPublishedAt"] = last_published_at
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if name is not UNSET:
            field_dict["name"] = name
        if qualified is not UNSET:
            field_dict["qualified"] = qualified
        if ranked is not UNSET:
            field_dict["ranked"] = ranked
        if stats is not UNSET:
            field_dict["stats"] = stats
        if tags is not UNSET:
            field_dict["tags"] = tags
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if uploaded is not UNSET:
            field_dict["uploaded"] = uploaded
        if uploader is not UNSET:
            field_dict["uploader"] = uploader
        if versions is not UNSET:
            field_dict["versions"] = versions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.map_detail_metadata import MapDetailMetadata
        from ..models.map_stats import MapStats
        from ..models.map_version import MapVersion
        from ..models.user_detail import UserDetail

        d = src_dict.copy()
        automapper = d.pop("automapper", UNSET)

        bl_qualified = d.pop("blQualified", UNSET)

        bl_ranked = d.pop("blRanked", UNSET)

        bookmarked = d.pop("bookmarked", UNSET)

        collaborators = []
        _collaborators = d.pop("collaborators", UNSET)
        for collaborators_item_data in _collaborators or []:
            collaborators_item = UserDetail.from_dict(collaborators_item_data)

            collaborators.append(collaborators_item)

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

        _declared_ai = d.pop("declaredAi", UNSET)
        declared_ai: Union[Unset, MapDetailDeclaredAi]
        if isinstance(_declared_ai, Unset):
            declared_ai = UNSET
        else:
            declared_ai = MapDetailDeclaredAi(_declared_ai)

        _deleted_at = d.pop("deletedAt", UNSET)
        deleted_at: Union[Unset, datetime.datetime]
        if isinstance(_deleted_at, Unset):
            deleted_at = UNSET
        else:
            deleted_at = isoparse(_deleted_at)

        description = d.pop("description", UNSET)

        id = d.pop("id", UNSET)

        _last_published_at = d.pop("lastPublishedAt", UNSET)
        last_published_at: Union[Unset, datetime.datetime]
        if isinstance(_last_published_at, Unset):
            last_published_at = UNSET
        else:
            last_published_at = isoparse(_last_published_at)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, MapDetailMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = MapDetailMetadata.from_dict(_metadata)

        name = d.pop("name", UNSET)

        qualified = d.pop("qualified", UNSET)

        ranked = d.pop("ranked", UNSET)

        _stats = d.pop("stats", UNSET)
        stats: Union[Unset, MapStats]
        if isinstance(_stats, Unset):
            stats = UNSET
        else:
            stats = MapStats.from_dict(_stats)

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in _tags or []:
            tags_item = MapDetailTagsItem(tags_item_data)

            tags.append(tags_item)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        _uploaded = d.pop("uploaded", UNSET)
        uploaded: Union[Unset, datetime.datetime]
        if isinstance(_uploaded, Unset):
            uploaded = UNSET
        else:
            uploaded = isoparse(_uploaded)

        _uploader = d.pop("uploader", UNSET)
        uploader: Union[Unset, UserDetail]
        if isinstance(_uploader, Unset):
            uploader = UNSET
        else:
            uploader = UserDetail.from_dict(_uploader)

        versions = []
        _versions = d.pop("versions", UNSET)
        for versions_item_data in _versions or []:
            versions_item = MapVersion.from_dict(versions_item_data)

            versions.append(versions_item)

        map_detail = cls(
            automapper=automapper,
            bl_qualified=bl_qualified,
            bl_ranked=bl_ranked,
            bookmarked=bookmarked,
            collaborators=collaborators,
            created_at=created_at,
            curated_at=curated_at,
            curator=curator,
            declared_ai=declared_ai,
            deleted_at=deleted_at,
            description=description,
            id=id,
            last_published_at=last_published_at,
            metadata=metadata,
            name=name,
            qualified=qualified,
            ranked=ranked,
            stats=stats,
            tags=tags,
            updated_at=updated_at,
            uploaded=uploaded,
            uploader=uploader,
            versions=versions,
        )

        map_detail.additional_properties = d
        return map_detail

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
