import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.user_detail_patreon import UserDetailPatreon
from ..models.user_detail_type import UserDetailType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_follow_data import UserFollowData
    from ..models.user_stats import UserStats


T = TypeVar("T", bound="UserDetail")


@_attrs_define
class UserDetail:
    """
    Attributes:
        admin (Union[Unset, bool]):
        avatar (Union[Unset, str]):
        curator (Union[Unset, bool]):
        curator_tab (Union[Unset, bool]):
        description (Union[Unset, str]):
        email (Union[Unset, str]):
        follow_data (Union[Unset, UserFollowData]):
        hash_ (Union[Unset, str]):
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        patreon (Union[Unset, UserDetailPatreon]):
        playlist_url (Union[Unset, str]):
        senior_curator (Union[Unset, bool]):
        stats (Union[Unset, UserStats]):
        suspended_at (Union[Unset, datetime.datetime]):
        testplay (Union[Unset, bool]):
        type (Union[Unset, UserDetailType]):
        unique_set (Union[Unset, bool]):
        upload_limit (Union[Unset, int]):
        verified_mapper (Union[Unset, bool]):
    """

    admin: Union[Unset, bool] = UNSET
    avatar: Union[Unset, str] = UNSET
    curator: Union[Unset, bool] = UNSET
    curator_tab: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    follow_data: Union[Unset, "UserFollowData"] = UNSET
    hash_: Union[Unset, str] = UNSET
    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    patreon: Union[Unset, UserDetailPatreon] = UNSET
    playlist_url: Union[Unset, str] = UNSET
    senior_curator: Union[Unset, bool] = UNSET
    stats: Union[Unset, "UserStats"] = UNSET
    suspended_at: Union[Unset, datetime.datetime] = UNSET
    testplay: Union[Unset, bool] = UNSET
    type: Union[Unset, UserDetailType] = UNSET
    unique_set: Union[Unset, bool] = UNSET
    upload_limit: Union[Unset, int] = UNSET
    verified_mapper: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        admin = self.admin

        avatar = self.avatar

        curator = self.curator

        curator_tab = self.curator_tab

        description = self.description

        email = self.email

        follow_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.follow_data, Unset):
            follow_data = self.follow_data.to_dict()

        hash_ = self.hash_

        id = self.id

        name = self.name

        patreon: Union[Unset, str] = UNSET
        if not isinstance(self.patreon, Unset):
            patreon = self.patreon.value

        playlist_url = self.playlist_url

        senior_curator = self.senior_curator

        stats: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stats, Unset):
            stats = self.stats.to_dict()

        suspended_at: Union[Unset, str] = UNSET
        if not isinstance(self.suspended_at, Unset):
            suspended_at = self.suspended_at.isoformat()

        testplay = self.testplay

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        unique_set = self.unique_set

        upload_limit = self.upload_limit

        verified_mapper = self.verified_mapper

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if admin is not UNSET:
            field_dict["admin"] = admin
        if avatar is not UNSET:
            field_dict["avatar"] = avatar
        if curator is not UNSET:
            field_dict["curator"] = curator
        if curator_tab is not UNSET:
            field_dict["curatorTab"] = curator_tab
        if description is not UNSET:
            field_dict["description"] = description
        if email is not UNSET:
            field_dict["email"] = email
        if follow_data is not UNSET:
            field_dict["followData"] = follow_data
        if hash_ is not UNSET:
            field_dict["hash"] = hash_
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if patreon is not UNSET:
            field_dict["patreon"] = patreon
        if playlist_url is not UNSET:
            field_dict["playlistUrl"] = playlist_url
        if senior_curator is not UNSET:
            field_dict["seniorCurator"] = senior_curator
        if stats is not UNSET:
            field_dict["stats"] = stats
        if suspended_at is not UNSET:
            field_dict["suspendedAt"] = suspended_at
        if testplay is not UNSET:
            field_dict["testplay"] = testplay
        if type is not UNSET:
            field_dict["type"] = type
        if unique_set is not UNSET:
            field_dict["uniqueSet"] = unique_set
        if upload_limit is not UNSET:
            field_dict["uploadLimit"] = upload_limit
        if verified_mapper is not UNSET:
            field_dict["verifiedMapper"] = verified_mapper

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_follow_data import UserFollowData
        from ..models.user_stats import UserStats

        d = src_dict.copy()
        admin = d.pop("admin", UNSET)

        avatar = d.pop("avatar", UNSET)

        curator = d.pop("curator", UNSET)

        curator_tab = d.pop("curatorTab", UNSET)

        description = d.pop("description", UNSET)

        email = d.pop("email", UNSET)

        _follow_data = d.pop("followData", UNSET)
        follow_data: Union[Unset, UserFollowData]
        if isinstance(_follow_data, Unset):
            follow_data = UNSET
        else:
            follow_data = UserFollowData.from_dict(_follow_data)

        hash_ = d.pop("hash", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _patreon = d.pop("patreon", UNSET)
        patreon: Union[Unset, UserDetailPatreon]
        if isinstance(_patreon, Unset):
            patreon = UNSET
        else:
            patreon = UserDetailPatreon(_patreon)

        playlist_url = d.pop("playlistUrl", UNSET)

        senior_curator = d.pop("seniorCurator", UNSET)

        _stats = d.pop("stats", UNSET)
        stats: Union[Unset, UserStats]
        if isinstance(_stats, Unset):
            stats = UNSET
        else:
            stats = UserStats.from_dict(_stats)

        _suspended_at = d.pop("suspendedAt", UNSET)
        suspended_at: Union[Unset, datetime.datetime]
        if isinstance(_suspended_at, Unset):
            suspended_at = UNSET
        else:
            suspended_at = isoparse(_suspended_at)

        testplay = d.pop("testplay", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, UserDetailType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = UserDetailType(_type)

        unique_set = d.pop("uniqueSet", UNSET)

        upload_limit = d.pop("uploadLimit", UNSET)

        verified_mapper = d.pop("verifiedMapper", UNSET)

        user_detail = cls(
            admin=admin,
            avatar=avatar,
            curator=curator,
            curator_tab=curator_tab,
            description=description,
            email=email,
            follow_data=follow_data,
            hash_=hash_,
            id=id,
            name=name,
            patreon=patreon,
            playlist_url=playlist_url,
            senior_curator=senior_curator,
            stats=stats,
            suspended_at=suspended_at,
            testplay=testplay,
            type=type,
            unique_set=unique_set,
            upload_limit=upload_limit,
            verified_mapper=verified_mapper,
        )

        user_detail.additional_properties = d
        return user_detail

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
