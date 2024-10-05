import datetime
from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.leaderboard_player import LeaderboardPlayer


T = TypeVar("T", bound="Score")


@_attrs_define
class Score:
    """
    Attributes:
        id (float):
        rank (float):
        base_score (float):
        modified_score (float):
        pp (float):
        weight (float):
        modifiers (str):
        multiplier (float):
        bad_cuts (float):
        missed_notes (float):
        max_combo (float):
        full_combo (bool):
        hmd (float):
        has_replay (bool):
        time_set (datetime.datetime):
        device_hmd (Union[None, str]):
        device_controller_left (Union[None, str]):
        device_controller_right (Union[None, str]):
        leaderboard_player_info (Union[Unset, LeaderboardPlayer]):
    """

    id: float
    rank: float
    base_score: float
    modified_score: float
    pp: float
    weight: float
    modifiers: str
    multiplier: float
    bad_cuts: float
    missed_notes: float
    max_combo: float
    full_combo: bool
    hmd: float
    has_replay: bool
    time_set: datetime.datetime
    device_hmd: Union[None, str]
    device_controller_left: Union[None, str]
    device_controller_right: Union[None, str]
    leaderboard_player_info: Union[Unset, "LeaderboardPlayer"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        rank = self.rank

        base_score = self.base_score

        modified_score = self.modified_score

        pp = self.pp

        weight = self.weight

        modifiers = self.modifiers

        multiplier = self.multiplier

        bad_cuts = self.bad_cuts

        missed_notes = self.missed_notes

        max_combo = self.max_combo

        full_combo = self.full_combo

        hmd = self.hmd

        has_replay = self.has_replay

        time_set = self.time_set.isoformat()

        device_hmd: Union[None, str]
        device_hmd = self.device_hmd

        device_controller_left: Union[None, str]
        device_controller_left = self.device_controller_left

        device_controller_right: Union[None, str]
        device_controller_right = self.device_controller_right

        leaderboard_player_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.leaderboard_player_info, Unset):
            leaderboard_player_info = self.leaderboard_player_info.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "rank": rank,
                "baseScore": base_score,
                "modifiedScore": modified_score,
                "pp": pp,
                "weight": weight,
                "modifiers": modifiers,
                "multiplier": multiplier,
                "badCuts": bad_cuts,
                "missedNotes": missed_notes,
                "maxCombo": max_combo,
                "fullCombo": full_combo,
                "hmd": hmd,
                "hasReplay": has_replay,
                "timeSet": time_set,
                "deviceHmd": device_hmd,
                "deviceControllerLeft": device_controller_left,
                "deviceControllerRight": device_controller_right,
            }
        )
        if leaderboard_player_info is not UNSET:
            field_dict["leaderboardPlayerInfo"] = leaderboard_player_info

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.leaderboard_player import LeaderboardPlayer

        d = src_dict.copy()
        id = d.pop("id")

        rank = d.pop("rank")

        base_score = d.pop("baseScore")

        modified_score = d.pop("modifiedScore")

        pp = d.pop("pp")

        weight = d.pop("weight")

        modifiers = d.pop("modifiers")

        multiplier = d.pop("multiplier")

        bad_cuts = d.pop("badCuts")

        missed_notes = d.pop("missedNotes")

        max_combo = d.pop("maxCombo")

        full_combo = d.pop("fullCombo")

        hmd = d.pop("hmd")

        has_replay = d.pop("hasReplay")

        time_set = isoparse(d.pop("timeSet"))

        def _parse_device_hmd(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        device_hmd = _parse_device_hmd(d.pop("deviceHmd"))

        def _parse_device_controller_left(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        device_controller_left = _parse_device_controller_left(d.pop("deviceControllerLeft"))

        def _parse_device_controller_right(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        device_controller_right = _parse_device_controller_right(d.pop("deviceControllerRight"))

        _leaderboard_player_info = d.pop("leaderboardPlayerInfo", UNSET)
        leaderboard_player_info: Union[Unset, LeaderboardPlayer]
        if isinstance(_leaderboard_player_info, Unset):
            leaderboard_player_info = UNSET
        elif _leaderboard_player_info is None:
            leaderboard_player_info = None  # Handle None value here
        else:
            leaderboard_player_info = LeaderboardPlayer.from_dict(_leaderboard_player_info)

        score = cls(
            id=id,
            rank=rank,
            base_score=base_score,
            modified_score=modified_score,
            pp=pp,
            weight=weight,
            modifiers=modifiers,
            multiplier=multiplier,
            bad_cuts=bad_cuts,
            missed_notes=missed_notes,
            max_combo=max_combo,
            full_combo=full_combo,
            hmd=hmd,
            has_replay=has_replay,
            time_set=time_set,
            device_hmd=device_hmd,
            device_controller_left=device_controller_left,
            device_controller_right=device_controller_right,
            leaderboard_player_info=leaderboard_player_info,
        )

        return score
