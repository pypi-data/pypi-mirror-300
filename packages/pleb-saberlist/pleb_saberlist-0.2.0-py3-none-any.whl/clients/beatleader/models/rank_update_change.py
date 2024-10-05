from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.modifiers_map import ModifiersMap


T = TypeVar("T", bound="RankUpdateChange")


@_attrs_define
class RankUpdateChange:
    """
    Attributes:
        id (Union[Unset, int]):
        timeset (Union[Unset, int]):
        player_id (Union[None, Unset, str]):
        old_keep (Union[Unset, bool]):
        old_stars (Union[Unset, float]):
        old_type (Union[Unset, int]):
        old_criteria_met (Union[Unset, int]):
        old_criteria_commentary (Union[None, Unset, str]):
        old_modifiers (Union[Unset, ModifiersMap]):
        new_keep (Union[Unset, bool]):
        new_stars (Union[Unset, float]):
        new_type (Union[Unset, int]):
        new_criteria_met (Union[Unset, int]):
        new_criteria_commentary (Union[None, Unset, str]):
        new_modifiers (Union[Unset, ModifiersMap]):
    """

    id: Union[Unset, int] = UNSET
    timeset: Union[Unset, int] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    old_keep: Union[Unset, bool] = UNSET
    old_stars: Union[Unset, float] = UNSET
    old_type: Union[Unset, int] = UNSET
    old_criteria_met: Union[Unset, int] = UNSET
    old_criteria_commentary: Union[None, Unset, str] = UNSET
    old_modifiers: Union[Unset, "ModifiersMap"] = UNSET
    new_keep: Union[Unset, bool] = UNSET
    new_stars: Union[Unset, float] = UNSET
    new_type: Union[Unset, int] = UNSET
    new_criteria_met: Union[Unset, int] = UNSET
    new_criteria_commentary: Union[None, Unset, str] = UNSET
    new_modifiers: Union[Unset, "ModifiersMap"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        timeset = self.timeset

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        old_keep = self.old_keep

        old_stars = self.old_stars

        old_type = self.old_type

        old_criteria_met = self.old_criteria_met

        old_criteria_commentary: Union[None, Unset, str]
        if isinstance(self.old_criteria_commentary, Unset):
            old_criteria_commentary = UNSET
        else:
            old_criteria_commentary = self.old_criteria_commentary

        old_modifiers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.old_modifiers, Unset):
            old_modifiers = self.old_modifiers.to_dict()

        new_keep = self.new_keep

        new_stars = self.new_stars

        new_type = self.new_type

        new_criteria_met = self.new_criteria_met

        new_criteria_commentary: Union[None, Unset, str]
        if isinstance(self.new_criteria_commentary, Unset):
            new_criteria_commentary = UNSET
        else:
            new_criteria_commentary = self.new_criteria_commentary

        new_modifiers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.new_modifiers, Unset):
            new_modifiers = self.new_modifiers.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if timeset is not UNSET:
            field_dict["timeset"] = timeset
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if old_keep is not UNSET:
            field_dict["oldKeep"] = old_keep
        if old_stars is not UNSET:
            field_dict["oldStars"] = old_stars
        if old_type is not UNSET:
            field_dict["oldType"] = old_type
        if old_criteria_met is not UNSET:
            field_dict["oldCriteriaMet"] = old_criteria_met
        if old_criteria_commentary is not UNSET:
            field_dict["oldCriteriaCommentary"] = old_criteria_commentary
        if old_modifiers is not UNSET:
            field_dict["oldModifiers"] = old_modifiers
        if new_keep is not UNSET:
            field_dict["newKeep"] = new_keep
        if new_stars is not UNSET:
            field_dict["newStars"] = new_stars
        if new_type is not UNSET:
            field_dict["newType"] = new_type
        if new_criteria_met is not UNSET:
            field_dict["newCriteriaMet"] = new_criteria_met
        if new_criteria_commentary is not UNSET:
            field_dict["newCriteriaCommentary"] = new_criteria_commentary
        if new_modifiers is not UNSET:
            field_dict["newModifiers"] = new_modifiers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.modifiers_map import ModifiersMap

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        timeset = d.pop("timeset", UNSET)

        def _parse_player_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_id = _parse_player_id(d.pop("playerId", UNSET))

        old_keep = d.pop("oldKeep", UNSET)

        old_stars = d.pop("oldStars", UNSET)

        old_type = d.pop("oldType", UNSET)

        old_criteria_met = d.pop("oldCriteriaMet", UNSET)

        def _parse_old_criteria_commentary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        old_criteria_commentary = _parse_old_criteria_commentary(d.pop("oldCriteriaCommentary", UNSET))

        _old_modifiers = d.pop("oldModifiers", UNSET)
        old_modifiers: Union[Unset, ModifiersMap]
        if isinstance(_old_modifiers, Unset):
            old_modifiers = UNSET
        else:
            old_modifiers = ModifiersMap.from_dict(_old_modifiers)

        new_keep = d.pop("newKeep", UNSET)

        new_stars = d.pop("newStars", UNSET)

        new_type = d.pop("newType", UNSET)

        new_criteria_met = d.pop("newCriteriaMet", UNSET)

        def _parse_new_criteria_commentary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        new_criteria_commentary = _parse_new_criteria_commentary(d.pop("newCriteriaCommentary", UNSET))

        _new_modifiers = d.pop("newModifiers", UNSET)
        new_modifiers: Union[Unset, ModifiersMap]
        if isinstance(_new_modifiers, Unset):
            new_modifiers = UNSET
        else:
            new_modifiers = ModifiersMap.from_dict(_new_modifiers)

        rank_update_change = cls(
            id=id,
            timeset=timeset,
            player_id=player_id,
            old_keep=old_keep,
            old_stars=old_stars,
            old_type=old_type,
            old_criteria_met=old_criteria_met,
            old_criteria_commentary=old_criteria_commentary,
            old_modifiers=old_modifiers,
            new_keep=new_keep,
            new_stars=new_stars,
            new_type=new_type,
            new_criteria_met=new_criteria_met,
            new_criteria_commentary=new_criteria_commentary,
            new_modifiers=new_modifiers,
        )

        return rank_update_change
