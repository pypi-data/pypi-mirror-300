from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.modifiers_map import ModifiersMap
    from ..models.modifiers_rating import ModifiersRating


T = TypeVar("T", bound="LeaderboardChange")


@_attrs_define
class LeaderboardChange:
    """
    Attributes:
        id (Union[Unset, int]):
        timeset (Union[Unset, int]):
        player_id (Union[None, Unset, str]):
        old_rankability (Union[Unset, float]):
        old_stars (Union[Unset, float]):
        old_acc_rating (Union[Unset, float]):
        old_pass_rating (Union[Unset, float]):
        old_tech_rating (Union[Unset, float]):
        old_type (Union[Unset, int]):
        old_criteria_met (Union[Unset, int]):
        old_modifiers (Union[Unset, ModifiersMap]):
        old_modifiers_rating (Union[Unset, ModifiersRating]):
        new_rankability (Union[Unset, float]):
        new_stars (Union[Unset, float]):
        new_acc_rating (Union[Unset, float]):
        new_pass_rating (Union[Unset, float]):
        new_tech_rating (Union[Unset, float]):
        new_type (Union[Unset, int]):
        new_criteria_met (Union[Unset, int]):
        new_modifiers (Union[Unset, ModifiersMap]):
        new_modifiers_rating (Union[Unset, ModifiersRating]):
    """

    id: Union[Unset, int] = UNSET
    timeset: Union[Unset, int] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    old_rankability: Union[Unset, float] = UNSET
    old_stars: Union[Unset, float] = UNSET
    old_acc_rating: Union[Unset, float] = UNSET
    old_pass_rating: Union[Unset, float] = UNSET
    old_tech_rating: Union[Unset, float] = UNSET
    old_type: Union[Unset, int] = UNSET
    old_criteria_met: Union[Unset, int] = UNSET
    old_modifiers: Union[Unset, "ModifiersMap"] = UNSET
    old_modifiers_rating: Union[Unset, "ModifiersRating"] = UNSET
    new_rankability: Union[Unset, float] = UNSET
    new_stars: Union[Unset, float] = UNSET
    new_acc_rating: Union[Unset, float] = UNSET
    new_pass_rating: Union[Unset, float] = UNSET
    new_tech_rating: Union[Unset, float] = UNSET
    new_type: Union[Unset, int] = UNSET
    new_criteria_met: Union[Unset, int] = UNSET
    new_modifiers: Union[Unset, "ModifiersMap"] = UNSET
    new_modifiers_rating: Union[Unset, "ModifiersRating"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        timeset = self.timeset

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        old_rankability = self.old_rankability

        old_stars = self.old_stars

        old_acc_rating = self.old_acc_rating

        old_pass_rating = self.old_pass_rating

        old_tech_rating = self.old_tech_rating

        old_type = self.old_type

        old_criteria_met = self.old_criteria_met

        old_modifiers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.old_modifiers, Unset):
            old_modifiers = self.old_modifiers.to_dict()

        old_modifiers_rating: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.old_modifiers_rating, Unset):
            old_modifiers_rating = self.old_modifiers_rating.to_dict()

        new_rankability = self.new_rankability

        new_stars = self.new_stars

        new_acc_rating = self.new_acc_rating

        new_pass_rating = self.new_pass_rating

        new_tech_rating = self.new_tech_rating

        new_type = self.new_type

        new_criteria_met = self.new_criteria_met

        new_modifiers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.new_modifiers, Unset):
            new_modifiers = self.new_modifiers.to_dict()

        new_modifiers_rating: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.new_modifiers_rating, Unset):
            new_modifiers_rating = self.new_modifiers_rating.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if timeset is not UNSET:
            field_dict["timeset"] = timeset
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if old_rankability is not UNSET:
            field_dict["oldRankability"] = old_rankability
        if old_stars is not UNSET:
            field_dict["oldStars"] = old_stars
        if old_acc_rating is not UNSET:
            field_dict["oldAccRating"] = old_acc_rating
        if old_pass_rating is not UNSET:
            field_dict["oldPassRating"] = old_pass_rating
        if old_tech_rating is not UNSET:
            field_dict["oldTechRating"] = old_tech_rating
        if old_type is not UNSET:
            field_dict["oldType"] = old_type
        if old_criteria_met is not UNSET:
            field_dict["oldCriteriaMet"] = old_criteria_met
        if old_modifiers is not UNSET:
            field_dict["oldModifiers"] = old_modifiers
        if old_modifiers_rating is not UNSET:
            field_dict["oldModifiersRating"] = old_modifiers_rating
        if new_rankability is not UNSET:
            field_dict["newRankability"] = new_rankability
        if new_stars is not UNSET:
            field_dict["newStars"] = new_stars
        if new_acc_rating is not UNSET:
            field_dict["newAccRating"] = new_acc_rating
        if new_pass_rating is not UNSET:
            field_dict["newPassRating"] = new_pass_rating
        if new_tech_rating is not UNSET:
            field_dict["newTechRating"] = new_tech_rating
        if new_type is not UNSET:
            field_dict["newType"] = new_type
        if new_criteria_met is not UNSET:
            field_dict["newCriteriaMet"] = new_criteria_met
        if new_modifiers is not UNSET:
            field_dict["newModifiers"] = new_modifiers
        if new_modifiers_rating is not UNSET:
            field_dict["newModifiersRating"] = new_modifiers_rating

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.modifiers_map import ModifiersMap
        from ..models.modifiers_rating import ModifiersRating

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

        old_rankability = d.pop("oldRankability", UNSET)

        old_stars = d.pop("oldStars", UNSET)

        old_acc_rating = d.pop("oldAccRating", UNSET)

        old_pass_rating = d.pop("oldPassRating", UNSET)

        old_tech_rating = d.pop("oldTechRating", UNSET)

        old_type = d.pop("oldType", UNSET)

        old_criteria_met = d.pop("oldCriteriaMet", UNSET)

        _old_modifiers = d.pop("oldModifiers", UNSET)
        old_modifiers: Union[Unset, ModifiersMap]
        if isinstance(_old_modifiers, Unset):
            old_modifiers = UNSET
        else:
            old_modifiers = ModifiersMap.from_dict(_old_modifiers)

        _old_modifiers_rating = d.pop("oldModifiersRating", UNSET)
        old_modifiers_rating: Union[Unset, ModifiersRating]
        if isinstance(_old_modifiers_rating, Unset):
            old_modifiers_rating = UNSET
        else:
            old_modifiers_rating = ModifiersRating.from_dict(_old_modifiers_rating)

        new_rankability = d.pop("newRankability", UNSET)

        new_stars = d.pop("newStars", UNSET)

        new_acc_rating = d.pop("newAccRating", UNSET)

        new_pass_rating = d.pop("newPassRating", UNSET)

        new_tech_rating = d.pop("newTechRating", UNSET)

        new_type = d.pop("newType", UNSET)

        new_criteria_met = d.pop("newCriteriaMet", UNSET)

        _new_modifiers = d.pop("newModifiers", UNSET)
        new_modifiers: Union[Unset, ModifiersMap]
        if isinstance(_new_modifiers, Unset):
            new_modifiers = UNSET
        else:
            new_modifiers = ModifiersMap.from_dict(_new_modifiers)

        _new_modifiers_rating = d.pop("newModifiersRating", UNSET)
        new_modifiers_rating: Union[Unset, ModifiersRating]
        if isinstance(_new_modifiers_rating, Unset):
            new_modifiers_rating = UNSET
        else:
            new_modifiers_rating = ModifiersRating.from_dict(_new_modifiers_rating)

        leaderboard_change = cls(
            id=id,
            timeset=timeset,
            player_id=player_id,
            old_rankability=old_rankability,
            old_stars=old_stars,
            old_acc_rating=old_acc_rating,
            old_pass_rating=old_pass_rating,
            old_tech_rating=old_tech_rating,
            old_type=old_type,
            old_criteria_met=old_criteria_met,
            old_modifiers=old_modifiers,
            old_modifiers_rating=old_modifiers_rating,
            new_rankability=new_rankability,
            new_stars=new_stars,
            new_acc_rating=new_acc_rating,
            new_pass_rating=new_pass_rating,
            new_tech_rating=new_tech_rating,
            new_type=new_type,
            new_criteria_met=new_criteria_met,
            new_modifiers=new_modifiers,
            new_modifiers_rating=new_modifiers_rating,
        )

        return leaderboard_change
