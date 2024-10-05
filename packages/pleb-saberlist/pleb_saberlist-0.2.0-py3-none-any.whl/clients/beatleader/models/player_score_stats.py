from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.hmd import HMD
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlayerScoreStats")


@_attrs_define
class PlayerScoreStats:
    """
    Attributes:
        id (Union[Unset, int]):
        total_score (Union[Unset, int]):
        total_unranked_score (Union[Unset, int]):
        total_ranked_score (Union[Unset, int]):
        last_score_time (Union[Unset, int]):
        last_unranked_score_time (Union[Unset, int]):
        last_ranked_score_time (Union[Unset, int]):
        average_ranked_accuracy (Union[Unset, float]):
        average_weighted_ranked_accuracy (Union[Unset, float]):
        average_unranked_accuracy (Union[Unset, float]):
        average_accuracy (Union[Unset, float]):
        median_ranked_accuracy (Union[Unset, float]):
        median_accuracy (Union[Unset, float]):
        top_ranked_accuracy (Union[Unset, float]):
        top_unranked_accuracy (Union[Unset, float]):
        top_accuracy (Union[Unset, float]):
        top_pp (Union[Unset, float]):
        top_bonus_pp (Union[Unset, float]):
        top_pass_pp (Union[Unset, float]):
        top_acc_pp (Union[Unset, float]):
        top_tech_pp (Union[Unset, float]):
        peak_rank (Union[Unset, float]):
        ranked_max_streak (Union[Unset, int]):
        unranked_max_streak (Union[Unset, int]):
        max_streak (Union[Unset, int]):
        average_left_timing (Union[Unset, float]):
        average_right_timing (Union[Unset, float]):
        ranked_play_count (Union[Unset, int]):
        unranked_play_count (Union[Unset, int]):
        total_play_count (Union[Unset, int]):
        ranked_improvements_count (Union[Unset, int]):
        unranked_improvements_count (Union[Unset, int]):
        total_improvements_count (Union[Unset, int]):
        ranked_top_1_count (Union[Unset, int]):
        unranked_top_1_count (Union[Unset, int]):
        top_1_count (Union[Unset, int]):
        ranked_top_1_score (Union[Unset, int]):
        unranked_top_1_score (Union[Unset, int]):
        top_1_score (Union[Unset, int]):
        average_ranked_rank (Union[Unset, float]):
        average_weighted_ranked_rank (Union[Unset, float]):
        average_unranked_rank (Union[Unset, float]):
        average_rank (Union[Unset, float]):
        ssp_plays (Union[Unset, int]):
        ss_plays (Union[Unset, int]):
        sp_plays (Union[Unset, int]):
        s_plays (Union[Unset, int]):
        a_plays (Union[Unset, int]):
        top_platform (Union[None, Unset, str]):
        top_hmd (Union[Unset, HMD]):
        top_percentile (Union[Unset, float]):
        country_top_percentile (Union[Unset, float]):
        daily_improvements (Union[Unset, int]):
        authorized_replay_watched (Union[Unset, int]):
        anonimus_replay_watched (Union[Unset, int]):
        watched_replays (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    total_score: Union[Unset, int] = UNSET
    total_unranked_score: Union[Unset, int] = UNSET
    total_ranked_score: Union[Unset, int] = UNSET
    last_score_time: Union[Unset, int] = UNSET
    last_unranked_score_time: Union[Unset, int] = UNSET
    last_ranked_score_time: Union[Unset, int] = UNSET
    average_ranked_accuracy: Union[Unset, float] = UNSET
    average_weighted_ranked_accuracy: Union[Unset, float] = UNSET
    average_unranked_accuracy: Union[Unset, float] = UNSET
    average_accuracy: Union[Unset, float] = UNSET
    median_ranked_accuracy: Union[Unset, float] = UNSET
    median_accuracy: Union[Unset, float] = UNSET
    top_ranked_accuracy: Union[Unset, float] = UNSET
    top_unranked_accuracy: Union[Unset, float] = UNSET
    top_accuracy: Union[Unset, float] = UNSET
    top_pp: Union[Unset, float] = UNSET
    top_bonus_pp: Union[Unset, float] = UNSET
    top_pass_pp: Union[Unset, float] = UNSET
    top_acc_pp: Union[Unset, float] = UNSET
    top_tech_pp: Union[Unset, float] = UNSET
    peak_rank: Union[Unset, float] = UNSET
    ranked_max_streak: Union[Unset, int] = UNSET
    unranked_max_streak: Union[Unset, int] = UNSET
    max_streak: Union[Unset, int] = UNSET
    average_left_timing: Union[Unset, float] = UNSET
    average_right_timing: Union[Unset, float] = UNSET
    ranked_play_count: Union[Unset, int] = UNSET
    unranked_play_count: Union[Unset, int] = UNSET
    total_play_count: Union[Unset, int] = UNSET
    ranked_improvements_count: Union[Unset, int] = UNSET
    unranked_improvements_count: Union[Unset, int] = UNSET
    total_improvements_count: Union[Unset, int] = UNSET
    ranked_top_1_count: Union[Unset, int] = UNSET
    unranked_top_1_count: Union[Unset, int] = UNSET
    top_1_count: Union[Unset, int] = UNSET
    ranked_top_1_score: Union[Unset, int] = UNSET
    unranked_top_1_score: Union[Unset, int] = UNSET
    top_1_score: Union[Unset, int] = UNSET
    average_ranked_rank: Union[Unset, float] = UNSET
    average_weighted_ranked_rank: Union[Unset, float] = UNSET
    average_unranked_rank: Union[Unset, float] = UNSET
    average_rank: Union[Unset, float] = UNSET
    ssp_plays: Union[Unset, int] = UNSET
    ss_plays: Union[Unset, int] = UNSET
    sp_plays: Union[Unset, int] = UNSET
    s_plays: Union[Unset, int] = UNSET
    a_plays: Union[Unset, int] = UNSET
    top_platform: Union[None, Unset, str] = UNSET
    top_hmd: Union[Unset, HMD] = UNSET
    top_percentile: Union[Unset, float] = UNSET
    country_top_percentile: Union[Unset, float] = UNSET
    daily_improvements: Union[Unset, int] = UNSET
    authorized_replay_watched: Union[Unset, int] = UNSET
    anonimus_replay_watched: Union[Unset, int] = UNSET
    watched_replays: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        total_score = self.total_score

        total_unranked_score = self.total_unranked_score

        total_ranked_score = self.total_ranked_score

        last_score_time = self.last_score_time

        last_unranked_score_time = self.last_unranked_score_time

        last_ranked_score_time = self.last_ranked_score_time

        average_ranked_accuracy = self.average_ranked_accuracy

        average_weighted_ranked_accuracy = self.average_weighted_ranked_accuracy

        average_unranked_accuracy = self.average_unranked_accuracy

        average_accuracy = self.average_accuracy

        median_ranked_accuracy = self.median_ranked_accuracy

        median_accuracy = self.median_accuracy

        top_ranked_accuracy = self.top_ranked_accuracy

        top_unranked_accuracy = self.top_unranked_accuracy

        top_accuracy = self.top_accuracy

        top_pp = self.top_pp

        top_bonus_pp = self.top_bonus_pp

        top_pass_pp = self.top_pass_pp

        top_acc_pp = self.top_acc_pp

        top_tech_pp = self.top_tech_pp

        peak_rank = self.peak_rank

        ranked_max_streak = self.ranked_max_streak

        unranked_max_streak = self.unranked_max_streak

        max_streak = self.max_streak

        average_left_timing = self.average_left_timing

        average_right_timing = self.average_right_timing

        ranked_play_count = self.ranked_play_count

        unranked_play_count = self.unranked_play_count

        total_play_count = self.total_play_count

        ranked_improvements_count = self.ranked_improvements_count

        unranked_improvements_count = self.unranked_improvements_count

        total_improvements_count = self.total_improvements_count

        ranked_top_1_count = self.ranked_top_1_count

        unranked_top_1_count = self.unranked_top_1_count

        top_1_count = self.top_1_count

        ranked_top_1_score = self.ranked_top_1_score

        unranked_top_1_score = self.unranked_top_1_score

        top_1_score = self.top_1_score

        average_ranked_rank = self.average_ranked_rank

        average_weighted_ranked_rank = self.average_weighted_ranked_rank

        average_unranked_rank = self.average_unranked_rank

        average_rank = self.average_rank

        ssp_plays = self.ssp_plays

        ss_plays = self.ss_plays

        sp_plays = self.sp_plays

        s_plays = self.s_plays

        a_plays = self.a_plays

        top_platform: Union[None, Unset, str]
        if isinstance(self.top_platform, Unset):
            top_platform = UNSET
        else:
            top_platform = self.top_platform

        top_hmd: Union[Unset, str] = UNSET
        if not isinstance(self.top_hmd, Unset):
            top_hmd = self.top_hmd.value

        top_percentile = self.top_percentile

        country_top_percentile = self.country_top_percentile

        daily_improvements = self.daily_improvements

        authorized_replay_watched = self.authorized_replay_watched

        anonimus_replay_watched = self.anonimus_replay_watched

        watched_replays = self.watched_replays

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if total_score is not UNSET:
            field_dict["totalScore"] = total_score
        if total_unranked_score is not UNSET:
            field_dict["totalUnrankedScore"] = total_unranked_score
        if total_ranked_score is not UNSET:
            field_dict["totalRankedScore"] = total_ranked_score
        if last_score_time is not UNSET:
            field_dict["lastScoreTime"] = last_score_time
        if last_unranked_score_time is not UNSET:
            field_dict["lastUnrankedScoreTime"] = last_unranked_score_time
        if last_ranked_score_time is not UNSET:
            field_dict["lastRankedScoreTime"] = last_ranked_score_time
        if average_ranked_accuracy is not UNSET:
            field_dict["averageRankedAccuracy"] = average_ranked_accuracy
        if average_weighted_ranked_accuracy is not UNSET:
            field_dict["averageWeightedRankedAccuracy"] = average_weighted_ranked_accuracy
        if average_unranked_accuracy is not UNSET:
            field_dict["averageUnrankedAccuracy"] = average_unranked_accuracy
        if average_accuracy is not UNSET:
            field_dict["averageAccuracy"] = average_accuracy
        if median_ranked_accuracy is not UNSET:
            field_dict["medianRankedAccuracy"] = median_ranked_accuracy
        if median_accuracy is not UNSET:
            field_dict["medianAccuracy"] = median_accuracy
        if top_ranked_accuracy is not UNSET:
            field_dict["topRankedAccuracy"] = top_ranked_accuracy
        if top_unranked_accuracy is not UNSET:
            field_dict["topUnrankedAccuracy"] = top_unranked_accuracy
        if top_accuracy is not UNSET:
            field_dict["topAccuracy"] = top_accuracy
        if top_pp is not UNSET:
            field_dict["topPp"] = top_pp
        if top_bonus_pp is not UNSET:
            field_dict["topBonusPP"] = top_bonus_pp
        if top_pass_pp is not UNSET:
            field_dict["topPassPP"] = top_pass_pp
        if top_acc_pp is not UNSET:
            field_dict["topAccPP"] = top_acc_pp
        if top_tech_pp is not UNSET:
            field_dict["topTechPP"] = top_tech_pp
        if peak_rank is not UNSET:
            field_dict["peakRank"] = peak_rank
        if ranked_max_streak is not UNSET:
            field_dict["rankedMaxStreak"] = ranked_max_streak
        if unranked_max_streak is not UNSET:
            field_dict["unrankedMaxStreak"] = unranked_max_streak
        if max_streak is not UNSET:
            field_dict["maxStreak"] = max_streak
        if average_left_timing is not UNSET:
            field_dict["averageLeftTiming"] = average_left_timing
        if average_right_timing is not UNSET:
            field_dict["averageRightTiming"] = average_right_timing
        if ranked_play_count is not UNSET:
            field_dict["rankedPlayCount"] = ranked_play_count
        if unranked_play_count is not UNSET:
            field_dict["unrankedPlayCount"] = unranked_play_count
        if total_play_count is not UNSET:
            field_dict["totalPlayCount"] = total_play_count
        if ranked_improvements_count is not UNSET:
            field_dict["rankedImprovementsCount"] = ranked_improvements_count
        if unranked_improvements_count is not UNSET:
            field_dict["unrankedImprovementsCount"] = unranked_improvements_count
        if total_improvements_count is not UNSET:
            field_dict["totalImprovementsCount"] = total_improvements_count
        if ranked_top_1_count is not UNSET:
            field_dict["rankedTop1Count"] = ranked_top_1_count
        if unranked_top_1_count is not UNSET:
            field_dict["unrankedTop1Count"] = unranked_top_1_count
        if top_1_count is not UNSET:
            field_dict["top1Count"] = top_1_count
        if ranked_top_1_score is not UNSET:
            field_dict["rankedTop1Score"] = ranked_top_1_score
        if unranked_top_1_score is not UNSET:
            field_dict["unrankedTop1Score"] = unranked_top_1_score
        if top_1_score is not UNSET:
            field_dict["top1Score"] = top_1_score
        if average_ranked_rank is not UNSET:
            field_dict["averageRankedRank"] = average_ranked_rank
        if average_weighted_ranked_rank is not UNSET:
            field_dict["averageWeightedRankedRank"] = average_weighted_ranked_rank
        if average_unranked_rank is not UNSET:
            field_dict["averageUnrankedRank"] = average_unranked_rank
        if average_rank is not UNSET:
            field_dict["averageRank"] = average_rank
        if ssp_plays is not UNSET:
            field_dict["sspPlays"] = ssp_plays
        if ss_plays is not UNSET:
            field_dict["ssPlays"] = ss_plays
        if sp_plays is not UNSET:
            field_dict["spPlays"] = sp_plays
        if s_plays is not UNSET:
            field_dict["sPlays"] = s_plays
        if a_plays is not UNSET:
            field_dict["aPlays"] = a_plays
        if top_platform is not UNSET:
            field_dict["topPlatform"] = top_platform
        if top_hmd is not UNSET:
            field_dict["topHMD"] = top_hmd
        if top_percentile is not UNSET:
            field_dict["topPercentile"] = top_percentile
        if country_top_percentile is not UNSET:
            field_dict["countryTopPercentile"] = country_top_percentile
        if daily_improvements is not UNSET:
            field_dict["dailyImprovements"] = daily_improvements
        if authorized_replay_watched is not UNSET:
            field_dict["authorizedReplayWatched"] = authorized_replay_watched
        if anonimus_replay_watched is not UNSET:
            field_dict["anonimusReplayWatched"] = anonimus_replay_watched
        if watched_replays is not UNSET:
            field_dict["watchedReplays"] = watched_replays

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        total_score = d.pop("totalScore", UNSET)

        total_unranked_score = d.pop("totalUnrankedScore", UNSET)

        total_ranked_score = d.pop("totalRankedScore", UNSET)

        last_score_time = d.pop("lastScoreTime", UNSET)

        last_unranked_score_time = d.pop("lastUnrankedScoreTime", UNSET)

        last_ranked_score_time = d.pop("lastRankedScoreTime", UNSET)

        average_ranked_accuracy = d.pop("averageRankedAccuracy", UNSET)

        average_weighted_ranked_accuracy = d.pop("averageWeightedRankedAccuracy", UNSET)

        average_unranked_accuracy = d.pop("averageUnrankedAccuracy", UNSET)

        average_accuracy = d.pop("averageAccuracy", UNSET)

        median_ranked_accuracy = d.pop("medianRankedAccuracy", UNSET)

        median_accuracy = d.pop("medianAccuracy", UNSET)

        top_ranked_accuracy = d.pop("topRankedAccuracy", UNSET)

        top_unranked_accuracy = d.pop("topUnrankedAccuracy", UNSET)

        top_accuracy = d.pop("topAccuracy", UNSET)

        top_pp = d.pop("topPp", UNSET)

        top_bonus_pp = d.pop("topBonusPP", UNSET)

        top_pass_pp = d.pop("topPassPP", UNSET)

        top_acc_pp = d.pop("topAccPP", UNSET)

        top_tech_pp = d.pop("topTechPP", UNSET)

        peak_rank = d.pop("peakRank", UNSET)

        ranked_max_streak = d.pop("rankedMaxStreak", UNSET)

        unranked_max_streak = d.pop("unrankedMaxStreak", UNSET)

        max_streak = d.pop("maxStreak", UNSET)

        average_left_timing = d.pop("averageLeftTiming", UNSET)

        average_right_timing = d.pop("averageRightTiming", UNSET)

        ranked_play_count = d.pop("rankedPlayCount", UNSET)

        unranked_play_count = d.pop("unrankedPlayCount", UNSET)

        total_play_count = d.pop("totalPlayCount", UNSET)

        ranked_improvements_count = d.pop("rankedImprovementsCount", UNSET)

        unranked_improvements_count = d.pop("unrankedImprovementsCount", UNSET)

        total_improvements_count = d.pop("totalImprovementsCount", UNSET)

        ranked_top_1_count = d.pop("rankedTop1Count", UNSET)

        unranked_top_1_count = d.pop("unrankedTop1Count", UNSET)

        top_1_count = d.pop("top1Count", UNSET)

        ranked_top_1_score = d.pop("rankedTop1Score", UNSET)

        unranked_top_1_score = d.pop("unrankedTop1Score", UNSET)

        top_1_score = d.pop("top1Score", UNSET)

        average_ranked_rank = d.pop("averageRankedRank", UNSET)

        average_weighted_ranked_rank = d.pop("averageWeightedRankedRank", UNSET)

        average_unranked_rank = d.pop("averageUnrankedRank", UNSET)

        average_rank = d.pop("averageRank", UNSET)

        ssp_plays = d.pop("sspPlays", UNSET)

        ss_plays = d.pop("ssPlays", UNSET)

        sp_plays = d.pop("spPlays", UNSET)

        s_plays = d.pop("sPlays", UNSET)

        a_plays = d.pop("aPlays", UNSET)

        def _parse_top_platform(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        top_platform = _parse_top_platform(d.pop("topPlatform", UNSET))

        _top_hmd = d.pop("topHMD", UNSET)
        top_hmd: Union[Unset, HMD]
        if isinstance(_top_hmd, Unset):
            top_hmd = UNSET
        else:
            top_hmd = HMD(_top_hmd)

        top_percentile = d.pop("topPercentile", UNSET)

        country_top_percentile = d.pop("countryTopPercentile", UNSET)

        daily_improvements = d.pop("dailyImprovements", UNSET)

        authorized_replay_watched = d.pop("authorizedReplayWatched", UNSET)

        anonimus_replay_watched = d.pop("anonimusReplayWatched", UNSET)

        watched_replays = d.pop("watchedReplays", UNSET)

        player_score_stats = cls(
            id=id,
            total_score=total_score,
            total_unranked_score=total_unranked_score,
            total_ranked_score=total_ranked_score,
            last_score_time=last_score_time,
            last_unranked_score_time=last_unranked_score_time,
            last_ranked_score_time=last_ranked_score_time,
            average_ranked_accuracy=average_ranked_accuracy,
            average_weighted_ranked_accuracy=average_weighted_ranked_accuracy,
            average_unranked_accuracy=average_unranked_accuracy,
            average_accuracy=average_accuracy,
            median_ranked_accuracy=median_ranked_accuracy,
            median_accuracy=median_accuracy,
            top_ranked_accuracy=top_ranked_accuracy,
            top_unranked_accuracy=top_unranked_accuracy,
            top_accuracy=top_accuracy,
            top_pp=top_pp,
            top_bonus_pp=top_bonus_pp,
            top_pass_pp=top_pass_pp,
            top_acc_pp=top_acc_pp,
            top_tech_pp=top_tech_pp,
            peak_rank=peak_rank,
            ranked_max_streak=ranked_max_streak,
            unranked_max_streak=unranked_max_streak,
            max_streak=max_streak,
            average_left_timing=average_left_timing,
            average_right_timing=average_right_timing,
            ranked_play_count=ranked_play_count,
            unranked_play_count=unranked_play_count,
            total_play_count=total_play_count,
            ranked_improvements_count=ranked_improvements_count,
            unranked_improvements_count=unranked_improvements_count,
            total_improvements_count=total_improvements_count,
            ranked_top_1_count=ranked_top_1_count,
            unranked_top_1_count=unranked_top_1_count,
            top_1_count=top_1_count,
            ranked_top_1_score=ranked_top_1_score,
            unranked_top_1_score=unranked_top_1_score,
            top_1_score=top_1_score,
            average_ranked_rank=average_ranked_rank,
            average_weighted_ranked_rank=average_weighted_ranked_rank,
            average_unranked_rank=average_unranked_rank,
            average_rank=average_rank,
            ssp_plays=ssp_plays,
            ss_plays=ss_plays,
            sp_plays=sp_plays,
            s_plays=s_plays,
            a_plays=a_plays,
            top_platform=top_platform,
            top_hmd=top_hmd,
            top_percentile=top_percentile,
            country_top_percentile=country_top_percentile,
            daily_improvements=daily_improvements,
            authorized_replay_watched=authorized_replay_watched,
            anonimus_replay_watched=anonimus_replay_watched,
            watched_replays=watched_replays,
        )

        return player_score_stats
