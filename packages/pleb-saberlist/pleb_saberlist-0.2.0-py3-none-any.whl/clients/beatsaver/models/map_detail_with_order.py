from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.map_detail import MapDetail


T = TypeVar("T", bound="MapDetailWithOrder")


@_attrs_define
class MapDetailWithOrder:
    """
    Attributes:
        map_ (Union[Unset, MapDetail]):
        order (Union[Unset, Any]):
    """

    map_: Union[Unset, "MapDetail"] = UNSET
    order: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        map_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.map_, Unset):
            map_ = self.map_.to_dict()

        order = self.order

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if map_ is not UNSET:
            field_dict["map"] = map_
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.map_detail import MapDetail

        d = src_dict.copy()
        _map_ = d.pop("map", UNSET)
        map_: Union[Unset, MapDetail]
        if isinstance(_map_, Unset):
            map_ = UNSET
        else:
            map_ = MapDetail.from_dict(_map_)

        order = d.pop("order", UNSET)

        map_detail_with_order = cls(
            map_=map_,
            order=order,
        )

        map_detail_with_order.additional_properties = d
        return map_detail_with_order

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
