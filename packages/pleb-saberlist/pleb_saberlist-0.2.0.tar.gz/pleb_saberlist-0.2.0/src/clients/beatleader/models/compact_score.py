from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.controller_enum import ControllerEnum
from ..models.hmd import HMD
from ..types import UNSET, Unset

T = TypeVar("T", bound="CompactScore")


@_attrs_define
class CompactScore:
    """
    Attributes:
        id (Union[None, Unset, int]):
        base_score (Union[Unset, int]):
        modified_score (Union[Unset, int]):
        modifiers (Union[None, Unset, str]):
        full_combo (Union[Unset, bool]):
        max_combo (Union[Unset, int]):
        missed_notes (Union[Unset, int]):
        bad_cuts (Union[Unset, int]):
        hmd (Union[Unset, HMD]):
        controller (Union[Unset, ControllerEnum]):
        accuracy (Union[Unset, float]):
        pp (Union[None, Unset, float]):
        epoch_time (Union[Unset, int]):
    """

    id: Union[None, Unset, int] = UNSET
    base_score: Union[Unset, int] = UNSET
    modified_score: Union[Unset, int] = UNSET
    modifiers: Union[None, Unset, str] = UNSET
    full_combo: Union[Unset, bool] = UNSET
    max_combo: Union[Unset, int] = UNSET
    missed_notes: Union[Unset, int] = UNSET
    bad_cuts: Union[Unset, int] = UNSET
    hmd: Union[Unset, HMD] = UNSET
    controller: Union[Unset, ControllerEnum] = UNSET
    accuracy: Union[Unset, float] = UNSET
    pp: Union[None, Unset, float] = UNSET
    epoch_time: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id: Union[None, Unset, int]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        base_score = self.base_score

        modified_score = self.modified_score

        modifiers: Union[None, Unset, str]
        if isinstance(self.modifiers, Unset):
            modifiers = UNSET
        else:
            modifiers = self.modifiers

        full_combo = self.full_combo

        max_combo = self.max_combo

        missed_notes = self.missed_notes

        bad_cuts = self.bad_cuts

        hmd: Union[Unset, str] = UNSET
        if not isinstance(self.hmd, Unset):
            hmd = self.hmd.value

        controller: Union[Unset, str] = UNSET
        if not isinstance(self.controller, Unset):
            controller = self.controller.value

        accuracy = self.accuracy

        pp: Union[None, Unset, float]
        if isinstance(self.pp, Unset):
            pp = UNSET
        else:
            pp = self.pp

        epoch_time = self.epoch_time

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if base_score is not UNSET:
            field_dict["baseScore"] = base_score
        if modified_score is not UNSET:
            field_dict["modifiedScore"] = modified_score
        if modifiers is not UNSET:
            field_dict["modifiers"] = modifiers
        if full_combo is not UNSET:
            field_dict["fullCombo"] = full_combo
        if max_combo is not UNSET:
            field_dict["maxCombo"] = max_combo
        if missed_notes is not UNSET:
            field_dict["missedNotes"] = missed_notes
        if bad_cuts is not UNSET:
            field_dict["badCuts"] = bad_cuts
        if hmd is not UNSET:
            field_dict["hmd"] = hmd
        if controller is not UNSET:
            field_dict["controller"] = controller
        if accuracy is not UNSET:
            field_dict["accuracy"] = accuracy
        if pp is not UNSET:
            field_dict["pp"] = pp
        if epoch_time is not UNSET:
            field_dict["epochTime"] = epoch_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        id = _parse_id(d.pop("id", UNSET))

        base_score = d.pop("baseScore", UNSET)

        modified_score = d.pop("modifiedScore", UNSET)

        def _parse_modifiers(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        modifiers = _parse_modifiers(d.pop("modifiers", UNSET))

        full_combo = d.pop("fullCombo", UNSET)

        max_combo = d.pop("maxCombo", UNSET)

        missed_notes = d.pop("missedNotes", UNSET)

        bad_cuts = d.pop("badCuts", UNSET)

        _hmd = d.pop("hmd", UNSET)
        hmd: Union[Unset, HMD]
        if isinstance(_hmd, Unset):
            hmd = UNSET
        else:
            hmd = HMD(_hmd)

        _controller = d.pop("controller", UNSET)
        controller: Union[Unset, ControllerEnum]
        if isinstance(_controller, Unset):
            controller = UNSET
        else:
            controller = ControllerEnum(_controller)

        accuracy = d.pop("accuracy", UNSET)

        def _parse_pp(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        pp = _parse_pp(d.pop("pp", UNSET))

        epoch_time = d.pop("epochTime", UNSET)

        compact_score = cls(
            id=id,
            base_score=base_score,
            modified_score=modified_score,
            modifiers=modifiers,
            full_combo=full_combo,
            max_combo=max_combo,
            missed_notes=missed_notes,
            bad_cuts=bad_cuts,
            hmd=hmd,
            controller=controller,
            accuracy=accuracy,
            pp=pp,
            epoch_time=epoch_time,
        )

        return compact_score
