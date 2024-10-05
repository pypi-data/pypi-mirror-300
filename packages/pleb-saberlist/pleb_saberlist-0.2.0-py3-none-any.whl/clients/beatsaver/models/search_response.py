from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.map_detail import MapDetail


T = TypeVar("T", bound="SearchResponse")


@_attrs_define
class SearchResponse:
    """
    Attributes:
        docs (Union[Unset, List['MapDetail']]):
        redirect (Union[Unset, str]):
    """

    docs: Union[Unset, List["MapDetail"]] = UNSET
    redirect: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        docs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.docs, Unset):
            docs = []
            for docs_item_data in self.docs:
                docs_item = docs_item_data.to_dict()
                docs.append(docs_item)

        redirect = self.redirect

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if docs is not UNSET:
            field_dict["docs"] = docs
        if redirect is not UNSET:
            field_dict["redirect"] = redirect

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.map_detail import MapDetail

        d = src_dict.copy()
        docs = []
        _docs = d.pop("docs", UNSET)
        for docs_item_data in _docs or []:
            docs_item = MapDetail.from_dict(docs_item_data)

            docs.append(docs_item)

        redirect = d.pop("redirect", UNSET)

        search_response = cls(
            docs=docs,
            redirect=redirect,
        )

        search_response.additional_properties = d
        return search_response

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
