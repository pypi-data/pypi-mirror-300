from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AchievementLevel")


@_attrs_define
class AchievementLevel:
    """
    Attributes:
        id (Union[Unset, int]):
        image (Union[None, Unset, str]):
        small_image (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        detailed_description (Union[None, Unset, str]):
        color (Union[None, Unset, str]):
        value (Union[None, Unset, float]):
        level (Union[Unset, int]):
        achievement_description_id (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    image: Union[None, Unset, str] = UNSET
    small_image: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    detailed_description: Union[None, Unset, str] = UNSET
    color: Union[None, Unset, str] = UNSET
    value: Union[None, Unset, float] = UNSET
    level: Union[Unset, int] = UNSET
    achievement_description_id: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        small_image: Union[None, Unset, str]
        if isinstance(self.small_image, Unset):
            small_image = UNSET
        else:
            small_image = self.small_image

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        detailed_description: Union[None, Unset, str]
        if isinstance(self.detailed_description, Unset):
            detailed_description = UNSET
        else:
            detailed_description = self.detailed_description

        color: Union[None, Unset, str]
        if isinstance(self.color, Unset):
            color = UNSET
        else:
            color = self.color

        value: Union[None, Unset, float]
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        level = self.level

        achievement_description_id = self.achievement_description_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if image is not UNSET:
            field_dict["image"] = image
        if small_image is not UNSET:
            field_dict["smallImage"] = small_image
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if detailed_description is not UNSET:
            field_dict["detailedDescription"] = detailed_description
        if color is not UNSET:
            field_dict["color"] = color
        if value is not UNSET:
            field_dict["value"] = value
        if level is not UNSET:
            field_dict["level"] = level
        if achievement_description_id is not UNSET:
            field_dict["achievementDescriptionId"] = achievement_description_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        def _parse_small_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        small_image = _parse_small_image(d.pop("smallImage", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_detailed_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        detailed_description = _parse_detailed_description(d.pop("detailedDescription", UNSET))

        def _parse_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        color = _parse_color(d.pop("color", UNSET))

        def _parse_value(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        value = _parse_value(d.pop("value", UNSET))

        level = d.pop("level", UNSET)

        achievement_description_id = d.pop("achievementDescriptionId", UNSET)

        achievement_level = cls(
            id=id,
            image=image,
            small_image=small_image,
            name=name,
            description=description,
            detailed_description=detailed_description,
            color=color,
            value=value,
            level=level,
            achievement_description_id=achievement_description_id,
        )

        return achievement_level
