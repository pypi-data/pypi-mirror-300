from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.clan_response_full import ClanResponseFull
    from ..models.difficulty_response import DifficultyResponse
    from ..models.rank_qualification import RankQualification
    from ..models.rank_update import RankUpdate
    from ..models.score_response_with_acc import ScoreResponseWithAcc
    from ..models.song import Song


T = TypeVar("T", bound="LeaderboardInfoResponse")


@_attrs_define
class LeaderboardInfoResponse:
    """
    Attributes:
        id (Union[None, Unset, str]):
        song (Union[Unset, Song]):
        difficulty (Union[Unset, DifficultyResponse]):
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

    id: Union[None, Unset, str] = UNSET
    song: Union[Unset, "Song"] = UNSET
    difficulty: Union[Unset, "DifficultyResponse"] = UNSET
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
        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        song: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.song, Unset):
            song = self.song.to_dict()

        difficulty: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.difficulty, Unset):
            difficulty = self.difficulty.to_dict()

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
        if song is not UNSET:
            field_dict["song"] = song
        if difficulty is not UNSET:
            field_dict["difficulty"] = difficulty
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
        from ..models.difficulty_response import DifficultyResponse
        from ..models.rank_qualification import RankQualification
        from ..models.rank_update import RankUpdate
        from ..models.score_response_with_acc import ScoreResponseWithAcc
        from ..models.song import Song

        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        _song = d.pop("song", UNSET)
        song: Union[Unset, Song]
        if isinstance(_song, Unset):
            song = UNSET
        else:
            song = Song.from_dict(_song)

        _difficulty = d.pop("difficulty", UNSET)
        difficulty: Union[Unset, DifficultyResponse]
        if isinstance(_difficulty, Unset):
            difficulty = UNSET
        else:
            difficulty = DifficultyResponse.from_dict(_difficulty)

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

        leaderboard_info_response = cls(
            id=id,
            song=song,
            difficulty=difficulty,
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

        return leaderboard_info_response
