from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReplayOffsets")


@_attrs_define
class ReplayOffsets:
    """
    Attributes:
        id (Union[Unset, int]):
        frames (Union[Unset, int]):
        notes (Union[Unset, int]):
        walls (Union[Unset, int]):
        heights (Union[Unset, int]):
        pauses (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    frames: Union[Unset, int] = UNSET
    notes: Union[Unset, int] = UNSET
    walls: Union[Unset, int] = UNSET
    heights: Union[Unset, int] = UNSET
    pauses: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        frames = self.frames

        notes = self.notes

        walls = self.walls

        heights = self.heights

        pauses = self.pauses

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if frames is not UNSET:
            field_dict["frames"] = frames
        if notes is not UNSET:
            field_dict["notes"] = notes
        if walls is not UNSET:
            field_dict["walls"] = walls
        if heights is not UNSET:
            field_dict["heights"] = heights
        if pauses is not UNSET:
            field_dict["pauses"] = pauses

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        frames = d.pop("frames", UNSET)

        notes = d.pop("notes", UNSET)

        walls = d.pop("walls", UNSET)

        heights = d.pop("heights", UNSET)

        pauses = d.pop("pauses", UNSET)

        replay_offsets = cls(
            id=id,
            frames=frames,
            notes=notes,
            walls=walls,
            heights=heights,
            pauses=pauses,
        )

        return replay_offsets
