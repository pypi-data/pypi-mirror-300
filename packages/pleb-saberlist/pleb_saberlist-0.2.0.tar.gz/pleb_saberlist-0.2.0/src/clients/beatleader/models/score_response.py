from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.controller_enum import ControllerEnum
from ..models.hmd import HMD
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.player_response import PlayerResponse
    from ..models.rank_voting import RankVoting
    from ..models.replay_offsets import ReplayOffsets
    from ..models.score_improvement import ScoreImprovement
    from ..models.score_metadata import ScoreMetadata


T = TypeVar("T", bound="ScoreResponse")


@_attrs_define
class ScoreResponse:
    """
    Attributes:
        id (Union[None, Unset, int]):
        base_score (Union[Unset, int]):
        modified_score (Union[Unset, int]):
        accuracy (Union[Unset, float]):
        player_id (Union[None, Unset, str]):
        pp (Union[Unset, float]):
        bonus_pp (Union[Unset, float]):
        pass_pp (Union[Unset, float]):
        acc_pp (Union[Unset, float]):
        tech_pp (Union[Unset, float]):
        rank (Union[Unset, int]):
        country (Union[None, Unset, str]):
        fc_accuracy (Union[Unset, float]):
        fc_pp (Union[Unset, float]):
        weight (Union[Unset, float]):
        replay (Union[None, Unset, str]):
        modifiers (Union[None, Unset, str]):
        bad_cuts (Union[Unset, int]):
        missed_notes (Union[Unset, int]):
        bomb_cuts (Union[Unset, int]):
        walls_hit (Union[Unset, int]):
        pauses (Union[Unset, int]):
        full_combo (Union[Unset, bool]):
        platform (Union[None, Unset, str]):
        max_combo (Union[Unset, int]):
        max_streak (Union[None, Unset, int]):
        hmd (Union[Unset, HMD]):
        controller (Union[Unset, ControllerEnum]):
        leaderboard_id (Union[None, Unset, str]):
        timeset (Union[None, Unset, str]):
        timepost (Union[Unset, int]):
        replays_watched (Union[Unset, int]):
        play_count (Union[Unset, int]):
        last_try_time (Union[Unset, int]):
        priority (Union[Unset, int]):
        player (Union[Unset, PlayerResponse]):
        score_improvement (Union[Unset, ScoreImprovement]):
        rank_voting (Union[Unset, RankVoting]):
        metadata (Union[Unset, ScoreMetadata]):
        offsets (Union[Unset, ReplayOffsets]):
    """

    id: Union[None, Unset, int] = UNSET
    base_score: Union[Unset, int] = UNSET
    modified_score: Union[Unset, int] = UNSET
    accuracy: Union[Unset, float] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    pp: Union[Unset, float] = UNSET
    bonus_pp: Union[Unset, float] = UNSET
    pass_pp: Union[Unset, float] = UNSET
    acc_pp: Union[Unset, float] = UNSET
    tech_pp: Union[Unset, float] = UNSET
    rank: Union[Unset, int] = UNSET
    country: Union[None, Unset, str] = UNSET
    fc_accuracy: Union[Unset, float] = UNSET
    fc_pp: Union[Unset, float] = UNSET
    weight: Union[Unset, float] = UNSET
    replay: Union[None, Unset, str] = UNSET
    modifiers: Union[None, Unset, str] = UNSET
    bad_cuts: Union[Unset, int] = UNSET
    missed_notes: Union[Unset, int] = UNSET
    bomb_cuts: Union[Unset, int] = UNSET
    walls_hit: Union[Unset, int] = UNSET
    pauses: Union[Unset, int] = UNSET
    full_combo: Union[Unset, bool] = UNSET
    platform: Union[None, Unset, str] = UNSET
    max_combo: Union[Unset, int] = UNSET
    max_streak: Union[None, Unset, int] = UNSET
    hmd: Union[Unset, HMD] = UNSET
    controller: Union[Unset, ControllerEnum] = UNSET
    leaderboard_id: Union[None, Unset, str] = UNSET
    timeset: Union[None, Unset, str] = UNSET
    timepost: Union[Unset, int] = UNSET
    replays_watched: Union[Unset, int] = UNSET
    play_count: Union[Unset, int] = UNSET
    last_try_time: Union[Unset, int] = UNSET
    priority: Union[Unset, int] = UNSET
    player: Union[Unset, "PlayerResponse"] = UNSET
    score_improvement: Union[Unset, "ScoreImprovement"] = UNSET
    rank_voting: Union[Unset, "RankVoting"] = UNSET
    metadata: Union[Unset, "ScoreMetadata"] = UNSET
    offsets: Union[Unset, "ReplayOffsets"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id: Union[None, Unset, int]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        base_score = self.base_score

        modified_score = self.modified_score

        accuracy = self.accuracy

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        pp = self.pp

        bonus_pp = self.bonus_pp

        pass_pp = self.pass_pp

        acc_pp = self.acc_pp

        tech_pp = self.tech_pp

        rank = self.rank

        country: Union[None, Unset, str]
        if isinstance(self.country, Unset):
            country = UNSET
        else:
            country = self.country

        fc_accuracy = self.fc_accuracy

        fc_pp = self.fc_pp

        weight = self.weight

        replay: Union[None, Unset, str]
        if isinstance(self.replay, Unset):
            replay = UNSET
        else:
            replay = self.replay

        modifiers: Union[None, Unset, str]
        if isinstance(self.modifiers, Unset):
            modifiers = UNSET
        else:
            modifiers = self.modifiers

        bad_cuts = self.bad_cuts

        missed_notes = self.missed_notes

        bomb_cuts = self.bomb_cuts

        walls_hit = self.walls_hit

        pauses = self.pauses

        full_combo = self.full_combo

        platform: Union[None, Unset, str]
        if isinstance(self.platform, Unset):
            platform = UNSET
        else:
            platform = self.platform

        max_combo = self.max_combo

        max_streak: Union[None, Unset, int]
        if isinstance(self.max_streak, Unset):
            max_streak = UNSET
        else:
            max_streak = self.max_streak

        hmd: Union[Unset, str] = UNSET
        if not isinstance(self.hmd, Unset):
            hmd = self.hmd.value

        controller: Union[Unset, str] = UNSET
        if not isinstance(self.controller, Unset):
            controller = self.controller.value

        leaderboard_id: Union[None, Unset, str]
        if isinstance(self.leaderboard_id, Unset):
            leaderboard_id = UNSET
        else:
            leaderboard_id = self.leaderboard_id

        timeset: Union[None, Unset, str]
        if isinstance(self.timeset, Unset):
            timeset = UNSET
        else:
            timeset = self.timeset

        timepost = self.timepost

        replays_watched = self.replays_watched

        play_count = self.play_count

        last_try_time = self.last_try_time

        priority = self.priority

        player: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.player, Unset):
            player = self.player.to_dict()

        score_improvement: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.score_improvement, Unset):
            score_improvement = self.score_improvement.to_dict()

        rank_voting: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rank_voting, Unset):
            rank_voting = self.rank_voting.to_dict()

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        offsets: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.offsets, Unset):
            offsets = self.offsets.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if base_score is not UNSET:
            field_dict["baseScore"] = base_score
        if modified_score is not UNSET:
            field_dict["modifiedScore"] = modified_score
        if accuracy is not UNSET:
            field_dict["accuracy"] = accuracy
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if pp is not UNSET:
            field_dict["pp"] = pp
        if bonus_pp is not UNSET:
            field_dict["bonusPp"] = bonus_pp
        if pass_pp is not UNSET:
            field_dict["passPP"] = pass_pp
        if acc_pp is not UNSET:
            field_dict["accPP"] = acc_pp
        if tech_pp is not UNSET:
            field_dict["techPP"] = tech_pp
        if rank is not UNSET:
            field_dict["rank"] = rank
        if country is not UNSET:
            field_dict["country"] = country
        if fc_accuracy is not UNSET:
            field_dict["fcAccuracy"] = fc_accuracy
        if fc_pp is not UNSET:
            field_dict["fcPp"] = fc_pp
        if weight is not UNSET:
            field_dict["weight"] = weight
        if replay is not UNSET:
            field_dict["replay"] = replay
        if modifiers is not UNSET:
            field_dict["modifiers"] = modifiers
        if bad_cuts is not UNSET:
            field_dict["badCuts"] = bad_cuts
        if missed_notes is not UNSET:
            field_dict["missedNotes"] = missed_notes
        if bomb_cuts is not UNSET:
            field_dict["bombCuts"] = bomb_cuts
        if walls_hit is not UNSET:
            field_dict["wallsHit"] = walls_hit
        if pauses is not UNSET:
            field_dict["pauses"] = pauses
        if full_combo is not UNSET:
            field_dict["fullCombo"] = full_combo
        if platform is not UNSET:
            field_dict["platform"] = platform
        if max_combo is not UNSET:
            field_dict["maxCombo"] = max_combo
        if max_streak is not UNSET:
            field_dict["maxStreak"] = max_streak
        if hmd is not UNSET:
            field_dict["hmd"] = hmd
        if controller is not UNSET:
            field_dict["controller"] = controller
        if leaderboard_id is not UNSET:
            field_dict["leaderboardId"] = leaderboard_id
        if timeset is not UNSET:
            field_dict["timeset"] = timeset
        if timepost is not UNSET:
            field_dict["timepost"] = timepost
        if replays_watched is not UNSET:
            field_dict["replaysWatched"] = replays_watched
        if play_count is not UNSET:
            field_dict["playCount"] = play_count
        if last_try_time is not UNSET:
            field_dict["lastTryTime"] = last_try_time
        if priority is not UNSET:
            field_dict["priority"] = priority
        if player is not UNSET:
            field_dict["player"] = player
        if score_improvement is not UNSET:
            field_dict["scoreImprovement"] = score_improvement
        if rank_voting is not UNSET:
            field_dict["rankVoting"] = rank_voting
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if offsets is not UNSET:
            field_dict["offsets"] = offsets

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.player_response import PlayerResponse
        from ..models.rank_voting import RankVoting
        from ..models.replay_offsets import ReplayOffsets
        from ..models.score_improvement import ScoreImprovement
        from ..models.score_metadata import ScoreMetadata

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

        accuracy = d.pop("accuracy", UNSET)

        def _parse_player_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_id = _parse_player_id(d.pop("playerId", UNSET))

        pp = d.pop("pp", UNSET)

        bonus_pp = d.pop("bonusPp", UNSET)

        pass_pp = d.pop("passPP", UNSET)

        acc_pp = d.pop("accPP", UNSET)

        tech_pp = d.pop("techPP", UNSET)

        rank = d.pop("rank", UNSET)

        def _parse_country(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        country = _parse_country(d.pop("country", UNSET))

        fc_accuracy = d.pop("fcAccuracy", UNSET)

        fc_pp = d.pop("fcPp", UNSET)

        weight = d.pop("weight", UNSET)

        def _parse_replay(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        replay = _parse_replay(d.pop("replay", UNSET))

        def _parse_modifiers(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        modifiers = _parse_modifiers(d.pop("modifiers", UNSET))

        bad_cuts = d.pop("badCuts", UNSET)

        missed_notes = d.pop("missedNotes", UNSET)

        bomb_cuts = d.pop("bombCuts", UNSET)

        walls_hit = d.pop("wallsHit", UNSET)

        pauses = d.pop("pauses", UNSET)

        full_combo = d.pop("fullCombo", UNSET)

        def _parse_platform(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        platform = _parse_platform(d.pop("platform", UNSET))

        max_combo = d.pop("maxCombo", UNSET)

        def _parse_max_streak(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_streak = _parse_max_streak(d.pop("maxStreak", UNSET))

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

        def _parse_leaderboard_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        leaderboard_id = _parse_leaderboard_id(d.pop("leaderboardId", UNSET))

        def _parse_timeset(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        timeset = _parse_timeset(d.pop("timeset", UNSET))

        timepost = d.pop("timepost", UNSET)

        replays_watched = d.pop("replaysWatched", UNSET)

        play_count = d.pop("playCount", UNSET)

        last_try_time = d.pop("lastTryTime", UNSET)

        priority = d.pop("priority", UNSET)

        _player = d.pop("player", UNSET)
        player: Union[Unset, PlayerResponse]
        if isinstance(_player, Unset):
            player = UNSET
        else:
            player = PlayerResponse.from_dict(_player)

        _score_improvement = d.pop("scoreImprovement", UNSET)
        score_improvement: Union[Unset, ScoreImprovement]
        if isinstance(_score_improvement, Unset):
            score_improvement = UNSET
        else:
            score_improvement = ScoreImprovement.from_dict(_score_improvement)

        _rank_voting = d.pop("rankVoting", UNSET)
        rank_voting: Union[Unset, RankVoting]
        if isinstance(_rank_voting, Unset):
            rank_voting = UNSET
        else:
            rank_voting = RankVoting.from_dict(_rank_voting)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, ScoreMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ScoreMetadata.from_dict(_metadata)

        _offsets = d.pop("offsets", UNSET)
        offsets: Union[Unset, ReplayOffsets]
        if isinstance(_offsets, Unset):
            offsets = UNSET
        else:
            offsets = ReplayOffsets.from_dict(_offsets)

        score_response = cls(
            id=id,
            base_score=base_score,
            modified_score=modified_score,
            accuracy=accuracy,
            player_id=player_id,
            pp=pp,
            bonus_pp=bonus_pp,
            pass_pp=pass_pp,
            acc_pp=acc_pp,
            tech_pp=tech_pp,
            rank=rank,
            country=country,
            fc_accuracy=fc_accuracy,
            fc_pp=fc_pp,
            weight=weight,
            replay=replay,
            modifiers=modifiers,
            bad_cuts=bad_cuts,
            missed_notes=missed_notes,
            bomb_cuts=bomb_cuts,
            walls_hit=walls_hit,
            pauses=pauses,
            full_combo=full_combo,
            platform=platform,
            max_combo=max_combo,
            max_streak=max_streak,
            hmd=hmd,
            controller=controller,
            leaderboard_id=leaderboard_id,
            timeset=timeset,
            timepost=timepost,
            replays_watched=replays_watched,
            play_count=play_count,
            last_try_time=last_try_time,
            priority=priority,
            player=player,
            score_improvement=score_improvement,
            rank_voting=rank_voting,
            metadata=metadata,
            offsets=offsets,
        )

        return score_response
