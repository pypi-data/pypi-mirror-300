from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.voter_feedback import VoterFeedback


T = TypeVar("T", bound="RankVoting")


@_attrs_define
class RankVoting:
    """
    Attributes:
        score_id (Union[Unset, int]):
        player_id (Union[None, Unset, str]):
        hash_ (Union[None, Unset, str]):
        diff (Union[None, Unset, str]):
        mode (Union[None, Unset, str]):
        rankability (Union[Unset, float]):
        stars (Union[Unset, float]):
        type (Union[Unset, int]):
        timeset (Union[Unset, int]):
        feedbacks (Union[List['VoterFeedback'], None, Unset]):
    """

    score_id: Union[Unset, int] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    hash_: Union[None, Unset, str] = UNSET
    diff: Union[None, Unset, str] = UNSET
    mode: Union[None, Unset, str] = UNSET
    rankability: Union[Unset, float] = UNSET
    stars: Union[Unset, float] = UNSET
    type: Union[Unset, int] = UNSET
    timeset: Union[Unset, int] = UNSET
    feedbacks: Union[List["VoterFeedback"], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        score_id = self.score_id

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        hash_: Union[None, Unset, str]
        if isinstance(self.hash_, Unset):
            hash_ = UNSET
        else:
            hash_ = self.hash_

        diff: Union[None, Unset, str]
        if isinstance(self.diff, Unset):
            diff = UNSET
        else:
            diff = self.diff

        mode: Union[None, Unset, str]
        if isinstance(self.mode, Unset):
            mode = UNSET
        else:
            mode = self.mode

        rankability = self.rankability

        stars = self.stars

        type = self.type

        timeset = self.timeset

        feedbacks: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.feedbacks, Unset):
            feedbacks = UNSET
        elif isinstance(self.feedbacks, list):
            feedbacks = []
            for feedbacks_type_0_item_data in self.feedbacks:
                feedbacks_type_0_item = feedbacks_type_0_item_data.to_dict()
                feedbacks.append(feedbacks_type_0_item)

        else:
            feedbacks = self.feedbacks

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if score_id is not UNSET:
            field_dict["scoreId"] = score_id
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if hash_ is not UNSET:
            field_dict["hash"] = hash_
        if diff is not UNSET:
            field_dict["diff"] = diff
        if mode is not UNSET:
            field_dict["mode"] = mode
        if rankability is not UNSET:
            field_dict["rankability"] = rankability
        if stars is not UNSET:
            field_dict["stars"] = stars
        if type is not UNSET:
            field_dict["type"] = type
        if timeset is not UNSET:
            field_dict["timeset"] = timeset
        if feedbacks is not UNSET:
            field_dict["feedbacks"] = feedbacks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.voter_feedback import VoterFeedback

        d = src_dict.copy()
        score_id = d.pop("scoreId", UNSET)

        def _parse_player_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_id = _parse_player_id(d.pop("playerId", UNSET))

        def _parse_hash_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        hash_ = _parse_hash_(d.pop("hash", UNSET))

        def _parse_diff(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        diff = _parse_diff(d.pop("diff", UNSET))

        def _parse_mode(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mode = _parse_mode(d.pop("mode", UNSET))

        rankability = d.pop("rankability", UNSET)

        stars = d.pop("stars", UNSET)

        type = d.pop("type", UNSET)

        timeset = d.pop("timeset", UNSET)

        def _parse_feedbacks(data: object) -> Union[List["VoterFeedback"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                feedbacks_type_0 = []
                _feedbacks_type_0 = data
                for feedbacks_type_0_item_data in _feedbacks_type_0:
                    feedbacks_type_0_item = VoterFeedback.from_dict(feedbacks_type_0_item_data)

                    feedbacks_type_0.append(feedbacks_type_0_item)

                return feedbacks_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["VoterFeedback"], None, Unset], data)

        feedbacks = _parse_feedbacks(d.pop("feedbacks", UNSET))

        rank_voting = cls(
            score_id=score_id,
            player_id=player_id,
            hash_=hash_,
            diff=diff,
            mode=mode,
            rankability=rankability,
            stars=stars,
            type=type,
            timeset=timeset,
            feedbacks=feedbacks,
        )

        return rank_voting
