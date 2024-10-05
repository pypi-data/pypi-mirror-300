from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.modifiers_map import ModifiersMap
    from ..models.modifiers_rating import ModifiersRating
    from ..models.rank_update_change import RankUpdateChange


T = TypeVar("T", bound="RankUpdate")


@_attrs_define
class RankUpdate:
    """
    Attributes:
        id (Union[Unset, int]):
        timeset (Union[Unset, int]):
        rt_member (Union[None, Unset, str]):
        keep (Union[Unset, bool]):
        stars (Union[Unset, float]):
        pass_rating (Union[Unset, float]):
        tech_rating (Union[Unset, float]):
        predicted_acc (Union[Unset, float]):
        type (Union[Unset, int]):
        criteria_met (Union[Unset, int]):
        criteria_commentary (Union[None, Unset, str]):
        finished (Union[Unset, bool]):
        modifiers (Union[Unset, ModifiersMap]):
        modifiers_rating (Union[Unset, ModifiersRating]):
        changes (Union[List['RankUpdateChange'], None, Unset]):
    """

    id: Union[Unset, int] = UNSET
    timeset: Union[Unset, int] = UNSET
    rt_member: Union[None, Unset, str] = UNSET
    keep: Union[Unset, bool] = UNSET
    stars: Union[Unset, float] = UNSET
    pass_rating: Union[Unset, float] = UNSET
    tech_rating: Union[Unset, float] = UNSET
    predicted_acc: Union[Unset, float] = UNSET
    type: Union[Unset, int] = UNSET
    criteria_met: Union[Unset, int] = UNSET
    criteria_commentary: Union[None, Unset, str] = UNSET
    finished: Union[Unset, bool] = UNSET
    modifiers: Union[Unset, "ModifiersMap"] = UNSET
    modifiers_rating: Union[Unset, "ModifiersRating"] = UNSET
    changes: Union[List["RankUpdateChange"], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        timeset = self.timeset

        rt_member: Union[None, Unset, str]
        if isinstance(self.rt_member, Unset):
            rt_member = UNSET
        else:
            rt_member = self.rt_member

        keep = self.keep

        stars = self.stars

        pass_rating = self.pass_rating

        tech_rating = self.tech_rating

        predicted_acc = self.predicted_acc

        type = self.type

        criteria_met = self.criteria_met

        criteria_commentary: Union[None, Unset, str]
        if isinstance(self.criteria_commentary, Unset):
            criteria_commentary = UNSET
        else:
            criteria_commentary = self.criteria_commentary

        finished = self.finished

        modifiers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.modifiers, Unset):
            modifiers = self.modifiers.to_dict()

        modifiers_rating: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.modifiers_rating, Unset):
            modifiers_rating = self.modifiers_rating.to_dict()

        changes: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.changes, Unset):
            changes = UNSET
        elif isinstance(self.changes, list):
            changes = []
            for changes_type_0_item_data in self.changes:
                changes_type_0_item = changes_type_0_item_data.to_dict()
                changes.append(changes_type_0_item)

        else:
            changes = self.changes

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if timeset is not UNSET:
            field_dict["timeset"] = timeset
        if rt_member is not UNSET:
            field_dict["rtMember"] = rt_member
        if keep is not UNSET:
            field_dict["keep"] = keep
        if stars is not UNSET:
            field_dict["stars"] = stars
        if pass_rating is not UNSET:
            field_dict["passRating"] = pass_rating
        if tech_rating is not UNSET:
            field_dict["techRating"] = tech_rating
        if predicted_acc is not UNSET:
            field_dict["predictedAcc"] = predicted_acc
        if type is not UNSET:
            field_dict["type"] = type
        if criteria_met is not UNSET:
            field_dict["criteriaMet"] = criteria_met
        if criteria_commentary is not UNSET:
            field_dict["criteriaCommentary"] = criteria_commentary
        if finished is not UNSET:
            field_dict["finished"] = finished
        if modifiers is not UNSET:
            field_dict["modifiers"] = modifiers
        if modifiers_rating is not UNSET:
            field_dict["modifiersRating"] = modifiers_rating
        if changes is not UNSET:
            field_dict["changes"] = changes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.modifiers_map import ModifiersMap
        from ..models.modifiers_rating import ModifiersRating
        from ..models.rank_update_change import RankUpdateChange

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        timeset = d.pop("timeset", UNSET)

        def _parse_rt_member(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        rt_member = _parse_rt_member(d.pop("rtMember", UNSET))

        keep = d.pop("keep", UNSET)

        stars = d.pop("stars", UNSET)

        pass_rating = d.pop("passRating", UNSET)

        tech_rating = d.pop("techRating", UNSET)

        predicted_acc = d.pop("predictedAcc", UNSET)

        type = d.pop("type", UNSET)

        criteria_met = d.pop("criteriaMet", UNSET)

        def _parse_criteria_commentary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        criteria_commentary = _parse_criteria_commentary(d.pop("criteriaCommentary", UNSET))

        finished = d.pop("finished", UNSET)

        _modifiers = d.pop("modifiers", UNSET)
        modifiers: Union[Unset, ModifiersMap]
        if isinstance(_modifiers, Unset):
            modifiers = UNSET
        else:
            modifiers = ModifiersMap.from_dict(_modifiers)

        _modifiers_rating = d.pop("modifiersRating", UNSET)
        modifiers_rating: Union[Unset, ModifiersRating]
        if isinstance(_modifiers_rating, Unset):
            modifiers_rating = UNSET
        else:
            modifiers_rating = ModifiersRating.from_dict(_modifiers_rating)

        def _parse_changes(data: object) -> Union[List["RankUpdateChange"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                changes_type_0 = []
                _changes_type_0 = data
                for changes_type_0_item_data in _changes_type_0:
                    changes_type_0_item = RankUpdateChange.from_dict(changes_type_0_item_data)

                    changes_type_0.append(changes_type_0_item)

                return changes_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["RankUpdateChange"], None, Unset], data)

        changes = _parse_changes(d.pop("changes", UNSET))

        rank_update = cls(
            id=id,
            timeset=timeset,
            rt_member=rt_member,
            keep=keep,
            stars=stars,
            pass_rating=pass_rating,
            tech_rating=tech_rating,
            predicted_acc=predicted_acc,
            type=type,
            criteria_met=criteria_met,
            criteria_commentary=criteria_commentary,
            finished=finished,
            modifiers=modifiers,
            modifiers_rating=modifiers_rating,
            changes=changes,
        )

        return rank_update
