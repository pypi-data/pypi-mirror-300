from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.achievement_description import AchievementDescription
    from ..models.achievement_level import AchievementLevel


T = TypeVar("T", bound="Achievement")


@_attrs_define
class Achievement:
    """
    Attributes:
        id (Union[Unset, int]):
        player_id (Union[None, Unset, str]):
        achievement_description_id (Union[Unset, int]):
        achievement_description (Union[Unset, AchievementDescription]):
        level (Union[Unset, AchievementLevel]):
        timeset (Union[Unset, int]):
        count (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    achievement_description_id: Union[Unset, int] = UNSET
    achievement_description: Union[Unset, "AchievementDescription"] = UNSET
    level: Union[Unset, "AchievementLevel"] = UNSET
    timeset: Union[Unset, int] = UNSET
    count: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        achievement_description_id = self.achievement_description_id

        achievement_description: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.achievement_description, Unset):
            achievement_description = self.achievement_description.to_dict()

        level: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.level, Unset):
            level = self.level.to_dict()

        timeset = self.timeset

        count = self.count

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if achievement_description_id is not UNSET:
            field_dict["achievementDescriptionId"] = achievement_description_id
        if achievement_description is not UNSET:
            field_dict["achievementDescription"] = achievement_description
        if level is not UNSET:
            field_dict["level"] = level
        if timeset is not UNSET:
            field_dict["timeset"] = timeset
        if count is not UNSET:
            field_dict["count"] = count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.achievement_description import AchievementDescription
        from ..models.achievement_level import AchievementLevel

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_player_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_id = _parse_player_id(d.pop("playerId", UNSET))

        achievement_description_id = d.pop("achievementDescriptionId", UNSET)

        _achievement_description = d.pop("achievementDescription", UNSET)
        achievement_description: Union[Unset, AchievementDescription]
        if isinstance(_achievement_description, Unset):
            achievement_description = UNSET
        else:
            achievement_description = AchievementDescription.from_dict(_achievement_description)

        _level = d.pop("level", UNSET)
        level: Union[Unset, AchievementLevel]
        if isinstance(_level, Unset):
            level = UNSET
        else:
            level = AchievementLevel.from_dict(_level)

        timeset = d.pop("timeset", UNSET)

        count = d.pop("count", UNSET)

        achievement = cls(
            id=id,
            player_id=player_id,
            achievement_description_id=achievement_description_id,
            achievement_description=achievement_description,
            level=level,
            timeset=timeset,
            count=count,
        )

        return achievement
