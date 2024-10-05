import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_detail import UserDetail


T = TypeVar("T", bound="MapTestplay")


@_attrs_define
class MapTestplay:
    """
    Attributes:
        created_at (Union[Unset, datetime.datetime]):
        feedback (Union[Unset, str]):
        feedback_at (Union[Unset, datetime.datetime]):
        user (Union[Unset, UserDetail]):
        video (Union[Unset, str]):
    """

    created_at: Union[Unset, datetime.datetime] = UNSET
    feedback: Union[Unset, str] = UNSET
    feedback_at: Union[Unset, datetime.datetime] = UNSET
    user: Union[Unset, "UserDetail"] = UNSET
    video: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        feedback = self.feedback

        feedback_at: Union[Unset, str] = UNSET
        if not isinstance(self.feedback_at, Unset):
            feedback_at = self.feedback_at.isoformat()

        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        video = self.video

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if feedback_at is not UNSET:
            field_dict["feedbackAt"] = feedback_at
        if user is not UNSET:
            field_dict["user"] = user
        if video is not UNSET:
            field_dict["video"] = video

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_detail import UserDetail

        d = src_dict.copy()
        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        feedback = d.pop("feedback", UNSET)

        _feedback_at = d.pop("feedbackAt", UNSET)
        feedback_at: Union[Unset, datetime.datetime]
        if isinstance(_feedback_at, Unset):
            feedback_at = UNSET
        else:
            feedback_at = isoparse(_feedback_at)

        _user = d.pop("user", UNSET)
        user: Union[Unset, UserDetail]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = UserDetail.from_dict(_user)

        video = d.pop("video", UNSET)

        map_testplay = cls(
            created_at=created_at,
            feedback=feedback,
            feedback_at=feedback_at,
            user=user,
            video=video,
        )

        map_testplay.additional_properties = d
        return map_testplay

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
