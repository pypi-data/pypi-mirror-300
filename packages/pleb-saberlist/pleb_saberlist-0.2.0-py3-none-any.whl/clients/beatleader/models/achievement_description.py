from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.achievement_level import AchievementLevel


T = TypeVar("T", bound="AchievementDescription")


@_attrs_define
class AchievementDescription:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        link (Union[None, Unset, str]):
        levels (Union[List['AchievementLevel'], None, Unset]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    link: Union[None, Unset, str] = UNSET
    levels: Union[List["AchievementLevel"], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

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

        link: Union[None, Unset, str]
        if isinstance(self.link, Unset):
            link = UNSET
        else:
            link = self.link

        levels: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.levels, Unset):
            levels = UNSET
        elif isinstance(self.levels, list):
            levels = []
            for levels_type_0_item_data in self.levels:
                levels_type_0_item = levels_type_0_item_data.to_dict()
                levels.append(levels_type_0_item)

        else:
            levels = self.levels

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if link is not UNSET:
            field_dict["link"] = link
        if levels is not UNSET:
            field_dict["levels"] = levels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.achievement_level import AchievementLevel

        d = src_dict.copy()
        id = d.pop("id", UNSET)

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

        def _parse_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        link = _parse_link(d.pop("link", UNSET))

        def _parse_levels(data: object) -> Union[List["AchievementLevel"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                levels_type_0 = []
                _levels_type_0 = data
                for levels_type_0_item_data in _levels_type_0:
                    levels_type_0_item = AchievementLevel.from_dict(levels_type_0_item_data)

                    levels_type_0.append(levels_type_0_item)

                return levels_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["AchievementLevel"], None, Unset], data)

        levels = _parse_levels(d.pop("levels", UNSET))

        achievement_description = cls(
            id=id,
            name=name,
            description=description,
            link=link,
            levels=levels,
        )

        return achievement_description
