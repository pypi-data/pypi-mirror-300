from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="BestiesNominationResponse")


@_attrs_define
class BestiesNominationResponse:
    """
    Attributes:
        message (Union[None, Unset, str]):
    """

    message: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        message: Union[None, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message = _parse_message(d.pop("message", UNSET))

        besties_nomination_response = cls(
            message=message,
        )

        return besties_nomination_response
