from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.difficulty_status import DifficultyStatus
from ..models.requirements import Requirements
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.clan_response_full import ClanResponseFull
    from ..models.modifiers_map import ModifiersMap
    from ..models.modifiers_rating import ModifiersRating
    from ..models.rank_qualification import RankQualification
    from ..models.rank_update import RankUpdate
    from ..models.score_response_with_acc import ScoreResponseWithAcc


T = TypeVar("T", bound="MapDiffResponse")


@_attrs_define
class MapDiffResponse:
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
        bombs (Union[Unset, int]):
        walls (Union[Unset, int]):
        max_score (Union[Unset, int]):
        duration (Union[Unset, float]):
        requirements (Union[Unset, Requirements]):
        leaderboard_id (Union[None, Unset, str]):
        plays (Union[Unset, int]):
        positive_votes (Union[Unset, int]):
        star_votes (Union[Unset, int]):
        negative_votes (Union[Unset, int]):
        vote_stars (Union[Unset, float]):
        clan (Union[Unset, ClanResponseFull]):
        clan_ranking_contested (Union[Unset, bool]):
        my_score (Union[Unset, ScoreResponseWithAcc]):
        qualification (Union[Unset, RankQualification]):
        reweight (Union[Unset, RankUpdate]):
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
    bombs: Union[Unset, int] = UNSET
    walls: Union[Unset, int] = UNSET
    max_score: Union[Unset, int] = UNSET
    duration: Union[Unset, float] = UNSET
    requirements: Union[Unset, Requirements] = UNSET
    leaderboard_id: Union[None, Unset, str] = UNSET
    plays: Union[Unset, int] = UNSET
    positive_votes: Union[Unset, int] = UNSET
    star_votes: Union[Unset, int] = UNSET
    negative_votes: Union[Unset, int] = UNSET
    vote_stars: Union[Unset, float] = UNSET
    clan: Union[Unset, "ClanResponseFull"] = UNSET
    clan_ranking_contested: Union[Unset, bool] = UNSET
    my_score: Union[Unset, "ScoreResponseWithAcc"] = UNSET
    qualification: Union[Unset, "RankQualification"] = UNSET
    reweight: Union[Unset, "RankUpdate"] = UNSET

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

        bombs = self.bombs

        walls = self.walls

        max_score = self.max_score

        duration = self.duration

        requirements: Union[Unset, str] = UNSET
        if not isinstance(self.requirements, Unset):
            requirements = self.requirements.value

        leaderboard_id: Union[None, Unset, str]
        if isinstance(self.leaderboard_id, Unset):
            leaderboard_id = UNSET
        else:
            leaderboard_id = self.leaderboard_id

        plays = self.plays

        positive_votes = self.positive_votes

        star_votes = self.star_votes

        negative_votes = self.negative_votes

        vote_stars = self.vote_stars

        clan: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.clan, Unset):
            clan = self.clan.to_dict()

        clan_ranking_contested = self.clan_ranking_contested

        my_score: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.my_score, Unset):
            my_score = self.my_score.to_dict()

        qualification: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.qualification, Unset):
            qualification = self.qualification.to_dict()

        reweight: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.reweight, Unset):
            reweight = self.reweight.to_dict()

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
        if leaderboard_id is not UNSET:
            field_dict["leaderboardId"] = leaderboard_id
        if plays is not UNSET:
            field_dict["plays"] = plays
        if positive_votes is not UNSET:
            field_dict["positiveVotes"] = positive_votes
        if star_votes is not UNSET:
            field_dict["starVotes"] = star_votes
        if negative_votes is not UNSET:
            field_dict["negativeVotes"] = negative_votes
        if vote_stars is not UNSET:
            field_dict["voteStars"] = vote_stars
        if clan is not UNSET:
            field_dict["clan"] = clan
        if clan_ranking_contested is not UNSET:
            field_dict["clanRankingContested"] = clan_ranking_contested
        if my_score is not UNSET:
            field_dict["myScore"] = my_score
        if qualification is not UNSET:
            field_dict["qualification"] = qualification
        if reweight is not UNSET:
            field_dict["reweight"] = reweight

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.clan_response_full import ClanResponseFull
        from ..models.modifiers_map import ModifiersMap
        from ..models.modifiers_rating import ModifiersRating
        from ..models.rank_qualification import RankQualification
        from ..models.rank_update import RankUpdate
        from ..models.score_response_with_acc import ScoreResponseWithAcc

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

        def _parse_leaderboard_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        leaderboard_id = _parse_leaderboard_id(d.pop("leaderboardId", UNSET))

        plays = d.pop("plays", UNSET)

        positive_votes = d.pop("positiveVotes", UNSET)

        star_votes = d.pop("starVotes", UNSET)

        negative_votes = d.pop("negativeVotes", UNSET)

        vote_stars = d.pop("voteStars", UNSET)

        _clan = d.pop("clan", UNSET)
        clan: Union[Unset, ClanResponseFull]
        if isinstance(_clan, Unset):
            clan = UNSET
        else:
            clan = ClanResponseFull.from_dict(_clan)

        clan_ranking_contested = d.pop("clanRankingContested", UNSET)

        _my_score = d.pop("myScore", UNSET)
        my_score: Union[Unset, ScoreResponseWithAcc]
        if isinstance(_my_score, Unset):
            my_score = UNSET
        else:
            my_score = ScoreResponseWithAcc.from_dict(_my_score)

        _qualification = d.pop("qualification", UNSET)
        qualification: Union[Unset, RankQualification]
        if isinstance(_qualification, Unset):
            qualification = UNSET
        else:
            qualification = RankQualification.from_dict(_qualification)

        _reweight = d.pop("reweight", UNSET)
        reweight: Union[Unset, RankUpdate]
        if isinstance(_reweight, Unset):
            reweight = UNSET
        else:
            reweight = RankUpdate.from_dict(_reweight)

        map_diff_response = cls(
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
            bombs=bombs,
            walls=walls,
            max_score=max_score,
            duration=duration,
            requirements=requirements,
            leaderboard_id=leaderboard_id,
            plays=plays,
            positive_votes=positive_votes,
            star_votes=star_votes,
            negative_votes=negative_votes,
            vote_stars=vote_stars,
            clan=clan,
            clan_ranking_contested=clan_ranking_contested,
            my_score=my_score,
            qualification=qualification,
            reweight=reweight,
        )

        return map_diff_response
