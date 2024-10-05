from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.criteria_commentary import CriteriaCommentary
    from ..models.modifiers_map import ModifiersMap
    from ..models.modifiers_rating import ModifiersRating
    from ..models.qualification_change import QualificationChange
    from ..models.qualification_commentary import QualificationCommentary
    from ..models.qualification_vote import QualificationVote


T = TypeVar("T", bound="RankQualification")


@_attrs_define
class RankQualification:
    """
    Attributes:
        id (Union[Unset, int]):
        timeset (Union[Unset, int]):
        rt_member (Union[None, Unset, str]):
        criteria_timeset (Union[Unset, int]):
        criteria_met (Union[Unset, int]):
        criteria_checker (Union[None, Unset, str]):
        criteria_commentary (Union[None, Unset, str]):
        mapper_allowed (Union[Unset, bool]):
        mapper_id (Union[None, Unset, str]):
        mapper_qualification (Union[Unset, bool]):
        approval_timeset (Union[Unset, int]):
        approved (Union[Unset, bool]):
        approvers (Union[None, Unset, str]):
        criteria_check (Union[None, Unset, str]):
        modifiers (Union[Unset, ModifiersMap]):
        modifiers_rating (Union[Unset, ModifiersRating]):
        changes (Union[List['QualificationChange'], None, Unset]):
        comments (Union[List['QualificationCommentary'], None, Unset]):
        criteria_comments (Union[List['CriteriaCommentary'], None, Unset]):
        quality_vote (Union[Unset, int]):
        votes (Union[List['QualificationVote'], None, Unset]):
        discord_channel_id (Union[None, Unset, str]):
        discord_rt_channel_id (Union[None, Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    timeset: Union[Unset, int] = UNSET
    rt_member: Union[None, Unset, str] = UNSET
    criteria_timeset: Union[Unset, int] = UNSET
    criteria_met: Union[Unset, int] = UNSET
    criteria_checker: Union[None, Unset, str] = UNSET
    criteria_commentary: Union[None, Unset, str] = UNSET
    mapper_allowed: Union[Unset, bool] = UNSET
    mapper_id: Union[None, Unset, str] = UNSET
    mapper_qualification: Union[Unset, bool] = UNSET
    approval_timeset: Union[Unset, int] = UNSET
    approved: Union[Unset, bool] = UNSET
    approvers: Union[None, Unset, str] = UNSET
    criteria_check: Union[None, Unset, str] = UNSET
    modifiers: Union[Unset, "ModifiersMap"] = UNSET
    modifiers_rating: Union[Unset, "ModifiersRating"] = UNSET
    changes: Union[List["QualificationChange"], None, Unset] = UNSET
    comments: Union[List["QualificationCommentary"], None, Unset] = UNSET
    criteria_comments: Union[List["CriteriaCommentary"], None, Unset] = UNSET
    quality_vote: Union[Unset, int] = UNSET
    votes: Union[List["QualificationVote"], None, Unset] = UNSET
    discord_channel_id: Union[None, Unset, str] = UNSET
    discord_rt_channel_id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        timeset = self.timeset

        rt_member: Union[None, Unset, str]
        if isinstance(self.rt_member, Unset):
            rt_member = UNSET
        else:
            rt_member = self.rt_member

        criteria_timeset = self.criteria_timeset

        criteria_met = self.criteria_met

        criteria_checker: Union[None, Unset, str]
        if isinstance(self.criteria_checker, Unset):
            criteria_checker = UNSET
        else:
            criteria_checker = self.criteria_checker

        criteria_commentary: Union[None, Unset, str]
        if isinstance(self.criteria_commentary, Unset):
            criteria_commentary = UNSET
        else:
            criteria_commentary = self.criteria_commentary

        mapper_allowed = self.mapper_allowed

        mapper_id: Union[None, Unset, str]
        if isinstance(self.mapper_id, Unset):
            mapper_id = UNSET
        else:
            mapper_id = self.mapper_id

        mapper_qualification = self.mapper_qualification

        approval_timeset = self.approval_timeset

        approved = self.approved

        approvers: Union[None, Unset, str]
        if isinstance(self.approvers, Unset):
            approvers = UNSET
        else:
            approvers = self.approvers

        criteria_check: Union[None, Unset, str]
        if isinstance(self.criteria_check, Unset):
            criteria_check = UNSET
        else:
            criteria_check = self.criteria_check

        modifiers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.modifiers, Unset):
            modifiers = self.modifiers.to_dict()

        modifiers_rating: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.modifiers_rating, Unset):
            modifiers_rating = self.modifiers_rating.to_dict()

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

        comments: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.comments, Unset):
            comments = UNSET
        elif isinstance(self.comments, list):
            comments = []
            for comments_type_0_item_data in self.comments:
                comments_type_0_item = comments_type_0_item_data.to_dict()
                comments.append(comments_type_0_item)

        else:
            comments = self.comments

        criteria_comments: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.criteria_comments, Unset):
            criteria_comments = UNSET
        elif isinstance(self.criteria_comments, list):
            criteria_comments = []
            for criteria_comments_type_0_item_data in self.criteria_comments:
                criteria_comments_type_0_item = criteria_comments_type_0_item_data.to_dict()
                criteria_comments.append(criteria_comments_type_0_item)

        else:
            criteria_comments = self.criteria_comments

        quality_vote = self.quality_vote

        votes: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.votes, Unset):
            votes = UNSET
        elif isinstance(self.votes, list):
            votes = []
            for votes_type_0_item_data in self.votes:
                votes_type_0_item = votes_type_0_item_data.to_dict()
                votes.append(votes_type_0_item)

        else:
            votes = self.votes

        discord_channel_id: Union[None, Unset, str]
        if isinstance(self.discord_channel_id, Unset):
            discord_channel_id = UNSET
        else:
            discord_channel_id = self.discord_channel_id

        discord_rt_channel_id: Union[None, Unset, str]
        if isinstance(self.discord_rt_channel_id, Unset):
            discord_rt_channel_id = UNSET
        else:
            discord_rt_channel_id = self.discord_rt_channel_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if timeset is not UNSET:
            field_dict["timeset"] = timeset
        if rt_member is not UNSET:
            field_dict["rtMember"] = rt_member
        if criteria_timeset is not UNSET:
            field_dict["criteriaTimeset"] = criteria_timeset
        if criteria_met is not UNSET:
            field_dict["criteriaMet"] = criteria_met
        if criteria_checker is not UNSET:
            field_dict["criteriaChecker"] = criteria_checker
        if criteria_commentary is not UNSET:
            field_dict["criteriaCommentary"] = criteria_commentary
        if mapper_allowed is not UNSET:
            field_dict["mapperAllowed"] = mapper_allowed
        if mapper_id is not UNSET:
            field_dict["mapperId"] = mapper_id
        if mapper_qualification is not UNSET:
            field_dict["mapperQualification"] = mapper_qualification
        if approval_timeset is not UNSET:
            field_dict["approvalTimeset"] = approval_timeset
        if approved is not UNSET:
            field_dict["approved"] = approved
        if approvers is not UNSET:
            field_dict["approvers"] = approvers
        if criteria_check is not UNSET:
            field_dict["criteriaCheck"] = criteria_check
        if modifiers is not UNSET:
            field_dict["modifiers"] = modifiers
        if modifiers_rating is not UNSET:
            field_dict["modifiersRating"] = modifiers_rating
        if changes is not UNSET:
            field_dict["changes"] = changes
        if comments is not UNSET:
            field_dict["comments"] = comments
        if criteria_comments is not UNSET:
            field_dict["criteriaComments"] = criteria_comments
        if quality_vote is not UNSET:
            field_dict["qualityVote"] = quality_vote
        if votes is not UNSET:
            field_dict["votes"] = votes
        if discord_channel_id is not UNSET:
            field_dict["discordChannelId"] = discord_channel_id
        if discord_rt_channel_id is not UNSET:
            field_dict["discordRTChannelId"] = discord_rt_channel_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.criteria_commentary import CriteriaCommentary
        from ..models.modifiers_map import ModifiersMap
        from ..models.modifiers_rating import ModifiersRating
        from ..models.qualification_change import QualificationChange
        from ..models.qualification_commentary import QualificationCommentary
        from ..models.qualification_vote import QualificationVote

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        timeset = d.pop("timeset", UNSET)

        def _parse_rt_member(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        rt_member = _parse_rt_member(d.pop("rtMember", UNSET))

        criteria_timeset = d.pop("criteriaTimeset", UNSET)

        criteria_met = d.pop("criteriaMet", UNSET)

        def _parse_criteria_checker(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        criteria_checker = _parse_criteria_checker(d.pop("criteriaChecker", UNSET))

        def _parse_criteria_commentary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        criteria_commentary = _parse_criteria_commentary(d.pop("criteriaCommentary", UNSET))

        mapper_allowed = d.pop("mapperAllowed", UNSET)

        def _parse_mapper_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mapper_id = _parse_mapper_id(d.pop("mapperId", UNSET))

        mapper_qualification = d.pop("mapperQualification", UNSET)

        approval_timeset = d.pop("approvalTimeset", UNSET)

        approved = d.pop("approved", UNSET)

        def _parse_approvers(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        approvers = _parse_approvers(d.pop("approvers", UNSET))

        def _parse_criteria_check(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        criteria_check = _parse_criteria_check(d.pop("criteriaCheck", UNSET))

        _modifiers = d.pop("modifiers", UNSET)
        modifiers: Union[Unset, ModifiersMap]
        if isinstance(_modifiers, Unset):
            modifiers = UNSET
        else:
            modifiers = ModifiersMap.from_dict(_modifiers)

        _modifiers_rating = d.pop("modifiersRating", UNSET)
        modifiers_rating: Union[Unset, ModifiersRating]
        if isinstance(_modifiers_rating, Unset):
            modifiers_rating = UNSET
        else:
            modifiers_rating = ModifiersRating.from_dict(_modifiers_rating)

        def _parse_changes(data: object) -> Union[List["QualificationChange"], None, Unset]:
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
                    changes_type_0_item = QualificationChange.from_dict(changes_type_0_item_data)

                    changes_type_0.append(changes_type_0_item)

                return changes_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["QualificationChange"], None, Unset], data)

        changes = _parse_changes(d.pop("changes", UNSET))

        def _parse_comments(data: object) -> Union[List["QualificationCommentary"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                comments_type_0 = []
                _comments_type_0 = data
                for comments_type_0_item_data in _comments_type_0:
                    comments_type_0_item = QualificationCommentary.from_dict(comments_type_0_item_data)

                    comments_type_0.append(comments_type_0_item)

                return comments_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["QualificationCommentary"], None, Unset], data)

        comments = _parse_comments(d.pop("comments", UNSET))

        def _parse_criteria_comments(data: object) -> Union[List["CriteriaCommentary"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                criteria_comments_type_0 = []
                _criteria_comments_type_0 = data
                for criteria_comments_type_0_item_data in _criteria_comments_type_0:
                    criteria_comments_type_0_item = CriteriaCommentary.from_dict(criteria_comments_type_0_item_data)

                    criteria_comments_type_0.append(criteria_comments_type_0_item)

                return criteria_comments_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["CriteriaCommentary"], None, Unset], data)

        criteria_comments = _parse_criteria_comments(d.pop("criteriaComments", UNSET))

        quality_vote = d.pop("qualityVote", UNSET)

        def _parse_votes(data: object) -> Union[List["QualificationVote"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                votes_type_0 = []
                _votes_type_0 = data
                for votes_type_0_item_data in _votes_type_0:
                    votes_type_0_item = QualificationVote.from_dict(votes_type_0_item_data)

                    votes_type_0.append(votes_type_0_item)

                return votes_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["QualificationVote"], None, Unset], data)

        votes = _parse_votes(d.pop("votes", UNSET))

        def _parse_discord_channel_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        discord_channel_id = _parse_discord_channel_id(d.pop("discordChannelId", UNSET))

        def _parse_discord_rt_channel_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        discord_rt_channel_id = _parse_discord_rt_channel_id(d.pop("discordRTChannelId", UNSET))

        rank_qualification = cls(
            id=id,
            timeset=timeset,
            rt_member=rt_member,
            criteria_timeset=criteria_timeset,
            criteria_met=criteria_met,
            criteria_checker=criteria_checker,
            criteria_commentary=criteria_commentary,
            mapper_allowed=mapper_allowed,
            mapper_id=mapper_id,
            mapper_qualification=mapper_qualification,
            approval_timeset=approval_timeset,
            approved=approved,
            approvers=approvers,
            criteria_check=criteria_check,
            modifiers=modifiers,
            modifiers_rating=modifiers_rating,
            changes=changes,
            comments=comments,
            criteria_comments=criteria_comments,
            quality_vote=quality_vote,
            votes=votes,
            discord_channel_id=discord_channel_id,
            discord_rt_channel_id=discord_rt_channel_id,
        )

        return rank_qualification
