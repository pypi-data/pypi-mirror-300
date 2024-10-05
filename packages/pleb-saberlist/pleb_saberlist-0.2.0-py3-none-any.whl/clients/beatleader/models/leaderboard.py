from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.difficulty_description import DifficultyDescription
    from ..models.event_ranking import EventRanking
    from ..models.leaderboard_change import LeaderboardChange
    from ..models.rank_qualification import RankQualification
    from ..models.rank_update import RankUpdate
    from ..models.song import Song


T = TypeVar("T", bound="Leaderboard")


@_attrs_define
class Leaderboard:
    """
    Attributes:
        id (Union[None, Unset, str]):
        song_id (Union[None, Unset, str]):
        song (Union[Unset, Song]):
        difficulty (Union[Unset, DifficultyDescription]):
        qualification (Union[Unset, RankQualification]):
        reweight (Union[Unset, RankUpdate]):
        timestamp (Union[Unset, int]):
        changes (Union[List['LeaderboardChange'], None, Unset]):
        events (Union[List['EventRanking'], None, Unset]):
        plays (Union[Unset, int]):
        play_count (Union[Unset, int]):
        positive_votes (Union[Unset, int]):
        star_votes (Union[Unset, int]):
        negative_votes (Union[Unset, int]):
        vote_stars (Union[Unset, float]):
        clan_id (Union[None, Unset, int]):
        captured_time (Union[None, Unset, int]):
        clan_ranking_contested (Union[Unset, bool]):
    """

    id: Union[None, Unset, str] = UNSET
    song_id: Union[None, Unset, str] = UNSET
    song: Union[Unset, "Song"] = UNSET
    difficulty: Union[Unset, "DifficultyDescription"] = UNSET
    qualification: Union[Unset, "RankQualification"] = UNSET
    reweight: Union[Unset, "RankUpdate"] = UNSET
    timestamp: Union[Unset, int] = UNSET
    changes: Union[List["LeaderboardChange"], None, Unset] = UNSET
    events: Union[List["EventRanking"], None, Unset] = UNSET
    plays: Union[Unset, int] = UNSET
    play_count: Union[Unset, int] = UNSET
    positive_votes: Union[Unset, int] = UNSET
    star_votes: Union[Unset, int] = UNSET
    negative_votes: Union[Unset, int] = UNSET
    vote_stars: Union[Unset, float] = UNSET
    clan_id: Union[None, Unset, int] = UNSET
    captured_time: Union[None, Unset, int] = UNSET
    clan_ranking_contested: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        song_id: Union[None, Unset, str]
        if isinstance(self.song_id, Unset):
            song_id = UNSET
        else:
            song_id = self.song_id

        song: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.song, Unset):
            song = self.song.to_dict()

        difficulty: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.difficulty, Unset):
            difficulty = self.difficulty.to_dict()

        qualification: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.qualification, Unset):
            qualification = self.qualification.to_dict()

        reweight: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.reweight, Unset):
            reweight = self.reweight.to_dict()

        timestamp = self.timestamp

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

        events: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.events, Unset):
            events = UNSET
        elif isinstance(self.events, list):
            events = []
            for events_type_0_item_data in self.events:
                events_type_0_item = events_type_0_item_data.to_dict()
                events.append(events_type_0_item)

        else:
            events = self.events

        plays = self.plays

        play_count = self.play_count

        positive_votes = self.positive_votes

        star_votes = self.star_votes

        negative_votes = self.negative_votes

        vote_stars = self.vote_stars

        clan_id: Union[None, Unset, int]
        if isinstance(self.clan_id, Unset):
            clan_id = UNSET
        else:
            clan_id = self.clan_id

        captured_time: Union[None, Unset, int]
        if isinstance(self.captured_time, Unset):
            captured_time = UNSET
        else:
            captured_time = self.captured_time

        clan_ranking_contested = self.clan_ranking_contested

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if song_id is not UNSET:
            field_dict["songId"] = song_id
        if song is not UNSET:
            field_dict["song"] = song
        if difficulty is not UNSET:
            field_dict["difficulty"] = difficulty
        if qualification is not UNSET:
            field_dict["qualification"] = qualification
        if reweight is not UNSET:
            field_dict["reweight"] = reweight
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if changes is not UNSET:
            field_dict["changes"] = changes
        if events is not UNSET:
            field_dict["events"] = events
        if plays is not UNSET:
            field_dict["plays"] = plays
        if play_count is not UNSET:
            field_dict["playCount"] = play_count
        if positive_votes is not UNSET:
            field_dict["positiveVotes"] = positive_votes
        if star_votes is not UNSET:
            field_dict["starVotes"] = star_votes
        if negative_votes is not UNSET:
            field_dict["negativeVotes"] = negative_votes
        if vote_stars is not UNSET:
            field_dict["voteStars"] = vote_stars
        if clan_id is not UNSET:
            field_dict["clanId"] = clan_id
        if captured_time is not UNSET:
            field_dict["capturedTime"] = captured_time
        if clan_ranking_contested is not UNSET:
            field_dict["clanRankingContested"] = clan_ranking_contested

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.difficulty_description import DifficultyDescription
        from ..models.event_ranking import EventRanking
        from ..models.leaderboard_change import LeaderboardChange
        from ..models.rank_qualification import RankQualification
        from ..models.rank_update import RankUpdate
        from ..models.song import Song

        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_song_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        song_id = _parse_song_id(d.pop("songId", UNSET))

        _song = d.pop("song", UNSET)
        song: Union[Unset, Song]
        if isinstance(_song, Unset):
            song = UNSET
        else:
            song = Song.from_dict(_song)

        _difficulty = d.pop("difficulty", UNSET)
        difficulty: Union[Unset, DifficultyDescription]
        if isinstance(_difficulty, Unset):
            difficulty = UNSET
        else:
            difficulty = DifficultyDescription.from_dict(_difficulty)

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

        timestamp = d.pop("timestamp", UNSET)

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

        def _parse_events(data: object) -> Union[List["EventRanking"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                events_type_0 = []
                _events_type_0 = data
                for events_type_0_item_data in _events_type_0:
                    events_type_0_item = EventRanking.from_dict(events_type_0_item_data)

                    events_type_0.append(events_type_0_item)

                return events_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["EventRanking"], None, Unset], data)

        events = _parse_events(d.pop("events", UNSET))

        plays = d.pop("plays", UNSET)

        play_count = d.pop("playCount", UNSET)

        positive_votes = d.pop("positiveVotes", UNSET)

        star_votes = d.pop("starVotes", UNSET)

        negative_votes = d.pop("negativeVotes", UNSET)

        vote_stars = d.pop("voteStars", UNSET)

        def _parse_clan_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        clan_id = _parse_clan_id(d.pop("clanId", UNSET))

        def _parse_captured_time(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        captured_time = _parse_captured_time(d.pop("capturedTime", UNSET))

        clan_ranking_contested = d.pop("clanRankingContested", UNSET)

        leaderboard = cls(
            id=id,
            song_id=song_id,
            song=song,
            difficulty=difficulty,
            qualification=qualification,
            reweight=reweight,
            timestamp=timestamp,
            changes=changes,
            events=events,
            plays=plays,
            play_count=play_count,
            positive_votes=positive_votes,
            star_votes=star_votes,
            negative_votes=negative_votes,
            vote_stars=vote_stars,
            clan_id=clan_id,
            captured_time=captured_time,
            clan_ranking_contested=clan_ranking_contested,
        )

        return leaderboard
