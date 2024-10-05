from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.clan_ranking_response import ClanRankingResponse
    from ..models.clan_response_full import ClanResponseFull
    from ..models.difficulty_response import DifficultyResponse
    from ..models.featured_playlist import FeaturedPlaylist
    from ..models.leaderboard_change import LeaderboardChange
    from ..models.leaderboard_group_entry import LeaderboardGroupEntry
    from ..models.rank_qualification import RankQualification
    from ..models.rank_update import RankUpdate
    from ..models.score_response import ScoreResponse
    from ..models.song_response import SongResponse


T = TypeVar("T", bound="LeaderboardClanRankingResponse")


@_attrs_define
class LeaderboardClanRankingResponse:
    """
    Attributes:
        id (Union[None, Unset, str]):
        song (Union[Unset, SongResponse]):
        difficulty (Union[Unset, DifficultyResponse]):
        scores (Union[List['ScoreResponse'], None, Unset]):
        changes (Union[List['LeaderboardChange'], None, Unset]):
        featured_playlists (Union[List['FeaturedPlaylist'], None, Unset]):
        qualification (Union[Unset, RankQualification]):
        reweight (Union[Unset, RankUpdate]):
        leaderboard_group (Union[List['LeaderboardGroupEntry'], None, Unset]):
        plays (Union[Unset, int]):
        clan (Union[Unset, ClanResponseFull]):
        clan_ranking_contested (Union[Unset, bool]):
        clan_ranking (Union[List['ClanRankingResponse'], None, Unset]):
    """

    id: Union[None, Unset, str] = UNSET
    song: Union[Unset, "SongResponse"] = UNSET
    difficulty: Union[Unset, "DifficultyResponse"] = UNSET
    scores: Union[List["ScoreResponse"], None, Unset] = UNSET
    changes: Union[List["LeaderboardChange"], None, Unset] = UNSET
    featured_playlists: Union[List["FeaturedPlaylist"], None, Unset] = UNSET
    qualification: Union[Unset, "RankQualification"] = UNSET
    reweight: Union[Unset, "RankUpdate"] = UNSET
    leaderboard_group: Union[List["LeaderboardGroupEntry"], None, Unset] = UNSET
    plays: Union[Unset, int] = UNSET
    clan: Union[Unset, "ClanResponseFull"] = UNSET
    clan_ranking_contested: Union[Unset, bool] = UNSET
    clan_ranking: Union[List["ClanRankingResponse"], None, Unset] = UNSET

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

        scores: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.scores, Unset):
            scores = UNSET
        elif isinstance(self.scores, list):
            scores = []
            for scores_type_0_item_data in self.scores:
                scores_type_0_item = scores_type_0_item_data.to_dict()
                scores.append(scores_type_0_item)

        else:
            scores = self.scores

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

        featured_playlists: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.featured_playlists, Unset):
            featured_playlists = UNSET
        elif isinstance(self.featured_playlists, list):
            featured_playlists = []
            for featured_playlists_type_0_item_data in self.featured_playlists:
                featured_playlists_type_0_item = featured_playlists_type_0_item_data.to_dict()
                featured_playlists.append(featured_playlists_type_0_item)

        else:
            featured_playlists = self.featured_playlists

        qualification: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.qualification, Unset):
            qualification = self.qualification.to_dict()

        reweight: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.reweight, Unset):
            reweight = self.reweight.to_dict()

        leaderboard_group: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.leaderboard_group, Unset):
            leaderboard_group = UNSET
        elif isinstance(self.leaderboard_group, list):
            leaderboard_group = []
            for leaderboard_group_type_0_item_data in self.leaderboard_group:
                leaderboard_group_type_0_item = leaderboard_group_type_0_item_data.to_dict()
                leaderboard_group.append(leaderboard_group_type_0_item)

        else:
            leaderboard_group = self.leaderboard_group

        plays = self.plays

        clan: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.clan, Unset):
            clan = self.clan.to_dict()

        clan_ranking_contested = self.clan_ranking_contested

        clan_ranking: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.clan_ranking, Unset):
            clan_ranking = UNSET
        elif isinstance(self.clan_ranking, list):
            clan_ranking = []
            for clan_ranking_type_0_item_data in self.clan_ranking:
                clan_ranking_type_0_item = clan_ranking_type_0_item_data.to_dict()
                clan_ranking.append(clan_ranking_type_0_item)

        else:
            clan_ranking = self.clan_ranking

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if song is not UNSET:
            field_dict["song"] = song
        if difficulty is not UNSET:
            field_dict["difficulty"] = difficulty
        if scores is not UNSET:
            field_dict["scores"] = scores
        if changes is not UNSET:
            field_dict["changes"] = changes
        if featured_playlists is not UNSET:
            field_dict["featuredPlaylists"] = featured_playlists
        if qualification is not UNSET:
            field_dict["qualification"] = qualification
        if reweight is not UNSET:
            field_dict["reweight"] = reweight
        if leaderboard_group is not UNSET:
            field_dict["leaderboardGroup"] = leaderboard_group
        if plays is not UNSET:
            field_dict["plays"] = plays
        if clan is not UNSET:
            field_dict["clan"] = clan
        if clan_ranking_contested is not UNSET:
            field_dict["clanRankingContested"] = clan_ranking_contested
        if clan_ranking is not UNSET:
            field_dict["clanRanking"] = clan_ranking

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.clan_ranking_response import ClanRankingResponse
        from ..models.clan_response_full import ClanResponseFull
        from ..models.difficulty_response import DifficultyResponse
        from ..models.featured_playlist import FeaturedPlaylist
        from ..models.leaderboard_change import LeaderboardChange
        from ..models.leaderboard_group_entry import LeaderboardGroupEntry
        from ..models.rank_qualification import RankQualification
        from ..models.rank_update import RankUpdate
        from ..models.score_response import ScoreResponse
        from ..models.song_response import SongResponse

        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        _song = d.pop("song", UNSET)
        song: Union[Unset, SongResponse]
        if isinstance(_song, Unset):
            song = UNSET
        else:
            song = SongResponse.from_dict(_song)

        _difficulty = d.pop("difficulty", UNSET)
        difficulty: Union[Unset, DifficultyResponse]
        if isinstance(_difficulty, Unset):
            difficulty = UNSET
        else:
            difficulty = DifficultyResponse.from_dict(_difficulty)

        def _parse_scores(data: object) -> Union[List["ScoreResponse"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scores_type_0 = []
                _scores_type_0 = data
                for scores_type_0_item_data in _scores_type_0:
                    scores_type_0_item = ScoreResponse.from_dict(scores_type_0_item_data)

                    scores_type_0.append(scores_type_0_item)

                return scores_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ScoreResponse"], None, Unset], data)

        scores = _parse_scores(d.pop("scores", UNSET))

        def _parse_changes(data: object) -> Union[List["LeaderboardChange"], None, Unset]:
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
                    changes_type_0_item = LeaderboardChange.from_dict(changes_type_0_item_data)

                    changes_type_0.append(changes_type_0_item)

                return changes_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["LeaderboardChange"], None, Unset], data)

        changes = _parse_changes(d.pop("changes", UNSET))

        def _parse_featured_playlists(data: object) -> Union[List["FeaturedPlaylist"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                featured_playlists_type_0 = []
                _featured_playlists_type_0 = data
                for featured_playlists_type_0_item_data in _featured_playlists_type_0:
                    featured_playlists_type_0_item = FeaturedPlaylist.from_dict(featured_playlists_type_0_item_data)

                    featured_playlists_type_0.append(featured_playlists_type_0_item)

                return featured_playlists_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["FeaturedPlaylist"], None, Unset], data)

        featured_playlists = _parse_featured_playlists(d.pop("featuredPlaylists", UNSET))

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

        def _parse_leaderboard_group(data: object) -> Union[List["LeaderboardGroupEntry"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                leaderboard_group_type_0 = []
                _leaderboard_group_type_0 = data
                for leaderboard_group_type_0_item_data in _leaderboard_group_type_0:
                    leaderboard_group_type_0_item = LeaderboardGroupEntry.from_dict(leaderboard_group_type_0_item_data)

                    leaderboard_group_type_0.append(leaderboard_group_type_0_item)

                return leaderboard_group_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["LeaderboardGroupEntry"], None, Unset], data)

        leaderboard_group = _parse_leaderboard_group(d.pop("leaderboardGroup", UNSET))

        plays = d.pop("plays", UNSET)

        _clan = d.pop("clan", UNSET)
        clan: Union[Unset, ClanResponseFull]
        if isinstance(_clan, Unset):
            clan = UNSET
        else:
            clan = ClanResponseFull.from_dict(_clan)

        clan_ranking_contested = d.pop("clanRankingContested", UNSET)

        def _parse_clan_ranking(data: object) -> Union[List["ClanRankingResponse"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                clan_ranking_type_0 = []
                _clan_ranking_type_0 = data
                for clan_ranking_type_0_item_data in _clan_ranking_type_0:
                    clan_ranking_type_0_item = ClanRankingResponse.from_dict(clan_ranking_type_0_item_data)

                    clan_ranking_type_0.append(clan_ranking_type_0_item)

                return clan_ranking_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ClanRankingResponse"], None, Unset], data)

        clan_ranking = _parse_clan_ranking(d.pop("clanRanking", UNSET))

        leaderboard_clan_ranking_response = cls(
            id=id,
            song=song,
            difficulty=difficulty,
            scores=scores,
            changes=changes,
            featured_playlists=featured_playlists,
            qualification=qualification,
            reweight=reweight,
            leaderboard_group=leaderboard_group,
            plays=plays,
            clan=clan,
            clan_ranking_contested=clan_ranking_contested,
            clan_ranking=clan_ranking,
        )

        return leaderboard_clan_ranking_response
