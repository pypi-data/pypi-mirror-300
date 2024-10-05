from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.difficulty_status import DifficultyStatus
from ..models.requirements import Requirements
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.modifiers_map import ModifiersMap
    from ..models.modifiers_rating import ModifiersRating


T = TypeVar("T", bound="DifficultyDescription")


@_attrs_define
class DifficultyDescription:
    """
    Attributes:
        id (Union[Unset, int]):
        value (Union[Unset, int]):
        mode (Union[Unset, int]):
        difficulty_name (Union[None, Unset, str]):
        mode_name (Union[None, Unset, str]):
        status (Union[Unset, DifficultyStatus]): Represents the difficulty status of a map.
        modifier_values (Union[Unset, ModifiersMap]):
        modifiers_rating (Union[Unset, ModifiersRating]):
        nominated_time (Union[Unset, int]):
        qualified_time (Union[Unset, int]):
        ranked_time (Union[Unset, int]):
        speed_tags (Union[Unset, int]):
        style_tags (Union[Unset, int]):
        feature_tags (Union[Unset, int]):
        stars (Union[None, Unset, float]):
        predicted_acc (Union[None, Unset, float]):
        pass_rating (Union[None, Unset, float]):
        acc_rating (Union[None, Unset, float]):
        tech_rating (Union[None, Unset, float]):
        type (Union[Unset, int]):
        njs (Union[Unset, float]):
        nps (Union[Unset, float]):
        notes (Union[Unset, int]):
        chains (Union[Unset, int]):
        sliders (Union[Unset, int]):
        bombs (Union[Unset, int]):
        walls (Union[Unset, int]):
        max_score (Union[Unset, int]):
        duration (Union[Unset, float]):
        requirements (Union[Unset, Requirements]):
    """

    id: Union[Unset, int] = UNSET
    value: Union[Unset, int] = UNSET
    mode: Union[Unset, int] = UNSET
    difficulty_name: Union[None, Unset, str] = UNSET
    mode_name: Union[None, Unset, str] = UNSET
    status: Union[Unset, DifficultyStatus] = UNSET
    modifier_values: Union[Unset, "ModifiersMap"] = UNSET
    modifiers_rating: Union[Unset, "ModifiersRating"] = UNSET
    nominated_time: Union[Unset, int] = UNSET
    qualified_time: Union[Unset, int] = UNSET
    ranked_time: Union[Unset, int] = UNSET
    speed_tags: Union[Unset, int] = UNSET
    style_tags: Union[Unset, int] = UNSET
    feature_tags: Union[Unset, int] = UNSET
    stars: Union[None, Unset, float] = UNSET
    predicted_acc: Union[None, Unset, float] = UNSET
    pass_rating: Union[None, Unset, float] = UNSET
    acc_rating: Union[None, Unset, float] = UNSET
    tech_rating: Union[None, Unset, float] = UNSET
    type: Union[Unset, int] = UNSET
    njs: Union[Unset, float] = UNSET
    nps: Union[Unset, float] = UNSET
    notes: Union[Unset, int] = UNSET
    chains: Union[Unset, int] = UNSET
    sliders: Union[Unset, int] = UNSET
    bombs: Union[Unset, int] = UNSET
    walls: Union[Unset, int] = UNSET
    max_score: Union[Unset, int] = UNSET
    duration: Union[Unset, float] = UNSET
    requirements: Union[Unset, Requirements] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        value = self.value

        mode = self.mode

        difficulty_name: Union[None, Unset, str]
        if isinstance(self.difficulty_name, Unset):
            difficulty_name = UNSET
        else:
            difficulty_name = self.difficulty_name

        mode_name: Union[None, Unset, str]
        if isinstance(self.mode_name, Unset):
            mode_name = UNSET
        else:
            mode_name = self.mode_name

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        modifier_values: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.modifier_values, Unset):
            modifier_values = self.modifier_values.to_dict()

        modifiers_rating: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.modifiers_rating, Unset):
            modifiers_rating = self.modifiers_rating.to_dict()

        nominated_time = self.nominated_time

        qualified_time = self.qualified_time

        ranked_time = self.ranked_time

        speed_tags = self.speed_tags

        style_tags = self.style_tags

        feature_tags = self.feature_tags

        stars: Union[None, Unset, float]
        if isinstance(self.stars, Unset):
            stars = UNSET
        else:
            stars = self.stars

        predicted_acc: Union[None, Unset, float]
        if isinstance(self.predicted_acc, Unset):
            predicted_acc = UNSET
        else:
            predicted_acc = self.predicted_acc

        pass_rating: Union[None, Unset, float]
        if isinstance(self.pass_rating, Unset):
            pass_rating = UNSET
        else:
            pass_rating = self.pass_rating

        acc_rating: Union[None, Unset, float]
        if isinstance(self.acc_rating, Unset):
            acc_rating = UNSET
        else:
            acc_rating = self.acc_rating

        tech_rating: Union[None, Unset, float]
        if isinstance(self.tech_rating, Unset):
            tech_rating = UNSET
        else:
            tech_rating = self.tech_rating

        type = self.type

        njs = self.njs

        nps = self.nps

        notes = self.notes

        chains = self.chains

        sliders = self.sliders

        bombs = self.bombs

        walls = self.walls

        max_score = self.max_score

        duration = self.duration

        requirements: Union[Unset, str] = UNSET
        if not isinstance(self.requirements, Unset):
            requirements = self.requirements.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if value is not UNSET:
            field_dict["value"] = value
        if mode is not UNSET:
            field_dict["mode"] = mode
        if difficulty_name is not UNSET:
            field_dict["difficultyName"] = difficulty_name
        if mode_name is not UNSET:
            field_dict["modeName"] = mode_name
        if status is not UNSET:
            field_dict["status"] = status
        if modifier_values is not UNSET:
            field_dict["modifierValues"] = modifier_values
        if modifiers_rating is not UNSET:
            field_dict["modifiersRating"] = modifiers_rating
        if nominated_time is not UNSET:
            field_dict["nominatedTime"] = nominated_time
        if qualified_time is not UNSET:
            field_dict["qualifiedTime"] = qualified_time
        if ranked_time is not UNSET:
            field_dict["rankedTime"] = ranked_time
        if speed_tags is not UNSET:
            field_dict["speedTags"] = speed_tags
        if style_tags is not UNSET:
            field_dict["styleTags"] = style_tags
        if feature_tags is not UNSET:
            field_dict["featureTags"] = feature_tags
        if stars is not UNSET:
            field_dict["stars"] = stars
        if predicted_acc is not UNSET:
            field_dict["predictedAcc"] = predicted_acc
        if pass_rating is not UNSET:
            field_dict["passRating"] = pass_rating
        if acc_rating is not UNSET:
            field_dict["accRating"] = acc_rating
        if tech_rating is not UNSET:
            field_dict["techRating"] = tech_rating
        if type is not UNSET:
            field_dict["type"] = type
        if njs is not UNSET:
            field_dict["njs"] = njs
        if nps is not UNSET:
            field_dict["nps"] = nps
        if notes is not UNSET:
            field_dict["notes"] = notes
        if chains is not UNSET:
            field_dict["chains"] = chains
        if sliders is not UNSET:
            field_dict["sliders"] = sliders
        if bombs is not UNSET:
            field_dict["bombs"] = bombs
        if walls is not UNSET:
            field_dict["walls"] = walls
        if max_score is not UNSET:
            field_dict["maxScore"] = max_score
        if duration is not UNSET:
            field_dict["duration"] = duration
        if requirements is not UNSET:
            field_dict["requirements"] = requirements

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.modifiers_map import ModifiersMap
        from ..models.modifiers_rating import ModifiersRating

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        value = d.pop("value", UNSET)

        mode = d.pop("mode", UNSET)

        def _parse_difficulty_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        difficulty_name = _parse_difficulty_name(d.pop("difficultyName", UNSET))

        def _parse_mode_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mode_name = _parse_mode_name(d.pop("modeName", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, DifficultyStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = DifficultyStatus(_status)

        _modifier_values = d.pop("modifierValues", UNSET)
        modifier_values: Union[Unset, ModifiersMap]
        if isinstance(_modifier_values, Unset):
            modifier_values = UNSET
        else:
            modifier_values = ModifiersMap.from_dict(_modifier_values)

        _modifiers_rating = d.pop("modifiersRating", UNSET)
        modifiers_rating: Union[Unset, ModifiersRating]
        if isinstance(_modifiers_rating, Unset):
            modifiers_rating = UNSET
        else:
            modifiers_rating = ModifiersRating.from_dict(_modifiers_rating)

        nominated_time = d.pop("nominatedTime", UNSET)

        qualified_time = d.pop("qualifiedTime", UNSET)

        ranked_time = d.pop("rankedTime", UNSET)

        speed_tags = d.pop("speedTags", UNSET)

        style_tags = d.pop("styleTags", UNSET)

        feature_tags = d.pop("featureTags", UNSET)

        def _parse_stars(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        stars = _parse_stars(d.pop("stars", UNSET))

        def _parse_predicted_acc(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        predicted_acc = _parse_predicted_acc(d.pop("predictedAcc", UNSET))

        def _parse_pass_rating(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        pass_rating = _parse_pass_rating(d.pop("passRating", UNSET))

        def _parse_acc_rating(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        acc_rating = _parse_acc_rating(d.pop("accRating", UNSET))

        def _parse_tech_rating(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        tech_rating = _parse_tech_rating(d.pop("techRating", UNSET))

        type = d.pop("type", UNSET)

        njs = d.pop("njs", UNSET)

        nps = d.pop("nps", UNSET)

        notes = d.pop("notes", UNSET)

        chains = d.pop("chains", UNSET)

        sliders = d.pop("sliders", UNSET)

        bombs = d.pop("bombs", UNSET)

        walls = d.pop("walls", UNSET)

        max_score = d.pop("maxScore", UNSET)

        duration = d.pop("duration", UNSET)

        _requirements = d.pop("requirements", UNSET)
        requirements: Union[Unset, Requirements]
        if isinstance(_requirements, Unset):
            requirements = UNSET
        else:
            requirements = Requirements(_requirements)

        difficulty_description = cls(
            id=id,
            value=value,
            mode=mode,
            difficulty_name=difficulty_name,
            mode_name=mode_name,
            status=status,
            modifier_values=modifier_values,
            modifiers_rating=modifiers_rating,
            nominated_time=nominated_time,
            qualified_time=qualified_time,
            ranked_time=ranked_time,
            speed_tags=speed_tags,
            style_tags=style_tags,
            feature_tags=feature_tags,
            stars=stars,
            predicted_acc=predicted_acc,
            pass_rating=pass_rating,
            acc_rating=acc_rating,
            tech_rating=tech_rating,
            type=type,
            njs=njs,
            nps=nps,
            notes=notes,
            chains=chains,
            sliders=sliders,
            bombs=bombs,
            walls=walls,
            max_score=max_score,
            duration=duration,
            requirements=requirements,
        )

        return difficulty_description
