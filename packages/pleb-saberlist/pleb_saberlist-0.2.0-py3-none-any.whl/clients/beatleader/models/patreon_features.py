from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatreonFeatures")


@_attrs_define
class PatreonFeatures:
    """
    Attributes:
        id (Union[Unset, int]):
        bio (Union[None, Unset, str]):
        message (Union[None, Unset, str]):
        left_saber_color (Union[None, Unset, str]):
        right_saber_color (Union[None, Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    bio: Union[None, Unset, str] = UNSET
    message: Union[None, Unset, str] = UNSET
    left_saber_color: Union[None, Unset, str] = UNSET
    right_saber_color: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        bio: Union[None, Unset, str]
        if isinstance(self.bio, Unset):
            bio = UNSET
        else:
            bio = self.bio

        message: Union[None, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        left_saber_color: Union[None, Unset, str]
        if isinstance(self.left_saber_color, Unset):
            left_saber_color = UNSET
        else:
            left_saber_color = self.left_saber_color

        right_saber_color: Union[None, Unset, str]
        if isinstance(self.right_saber_color, Unset):
            right_saber_color = UNSET
        else:
            right_saber_color = self.right_saber_color

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if bio is not UNSET:
            field_dict["bio"] = bio
        if message is not UNSET:
            field_dict["message"] = message
        if left_saber_color is not UNSET:
            field_dict["leftSaberColor"] = left_saber_color
        if right_saber_color is not UNSET:
            field_dict["rightSaberColor"] = right_saber_color

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_bio(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bio = _parse_bio(d.pop("bio", UNSET))

        def _parse_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_left_saber_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        left_saber_color = _parse_left_saber_color(d.pop("leftSaberColor", UNSET))

        def _parse_right_saber_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        right_saber_color = _parse_right_saber_color(d.pop("rightSaberColor", UNSET))

        patreon_features = cls(
            id=id,
            bio=bio,
            message=message,
            left_saber_color=left_saber_color,
            right_saber_color=right_saber_color,
        )

        return patreon_features
