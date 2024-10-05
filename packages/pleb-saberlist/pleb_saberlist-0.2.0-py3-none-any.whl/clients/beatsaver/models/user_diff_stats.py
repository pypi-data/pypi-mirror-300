from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserDiffStats")


@_attrs_define
class UserDiffStats:
    """
    Attributes:
        easy (Union[Unset, int]):
        expert (Union[Unset, int]):
        expert_plus (Union[Unset, int]):
        hard (Union[Unset, int]):
        normal (Union[Unset, int]):
        total (Union[Unset, int]):
    """

    easy: Union[Unset, int] = UNSET
    expert: Union[Unset, int] = UNSET
    expert_plus: Union[Unset, int] = UNSET
    hard: Union[Unset, int] = UNSET
    normal: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        easy = self.easy

        expert = self.expert

        expert_plus = self.expert_plus

        hard = self.hard

        normal = self.normal

        total = self.total

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if easy is not UNSET:
            field_dict["easy"] = easy
        if expert is not UNSET:
            field_dict["expert"] = expert
        if expert_plus is not UNSET:
            field_dict["expertPlus"] = expert_plus
        if hard is not UNSET:
            field_dict["hard"] = hard
        if normal is not UNSET:
            field_dict["normal"] = normal
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        easy = d.pop("easy", UNSET)

        expert = d.pop("expert", UNSET)

        expert_plus = d.pop("expertPlus", UNSET)

        hard = d.pop("hard", UNSET)

        normal = d.pop("normal", UNSET)

        total = d.pop("total", UNSET)

        user_diff_stats = cls(
            easy=easy,
            expert=expert,
            expert_plus=expert_plus,
            hard=hard,
            normal=normal,
            total=total,
        )

        user_diff_stats.additional_properties = d
        return user_diff_stats

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
