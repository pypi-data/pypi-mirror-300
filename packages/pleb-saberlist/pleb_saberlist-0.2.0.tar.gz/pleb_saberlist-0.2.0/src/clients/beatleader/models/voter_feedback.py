from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="VoterFeedback")


@_attrs_define
class VoterFeedback:
    """
    Attributes:
        id (Union[Unset, int]):
        rt_member (Union[None, Unset, str]):
        value (Union[Unset, float]):
    """

    id: Union[Unset, int] = UNSET
    rt_member: Union[None, Unset, str] = UNSET
    value: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        rt_member: Union[None, Unset, str]
        if isinstance(self.rt_member, Unset):
            rt_member = UNSET
        else:
            rt_member = self.rt_member

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if rt_member is not UNSET:
            field_dict["rtMember"] = rt_member
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_rt_member(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        rt_member = _parse_rt_member(d.pop("rtMember", UNSET))

        value = d.pop("value", UNSET)

        voter_feedback = cls(
            id=id,
            rt_member=rt_member,
            value=value,
        )

        return voter_feedback
