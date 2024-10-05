from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.info_to_highlight import InfoToHighlight
from ..models.leaderboard_contexts import LeaderboardContexts
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScoreMetadata")


@_attrs_define
class ScoreMetadata:
    """
    Attributes:
        id (Union[Unset, int]):
        pinned_contexts (Union[Unset, LeaderboardContexts]):
        highlighted_info (Union[Unset, InfoToHighlight]):
        priority (Union[Unset, int]):
        description (Union[None, Unset, str]):
        link_service (Union[None, Unset, str]):
        link_service_icon (Union[None, Unset, str]):
        link (Union[None, Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    pinned_contexts: Union[Unset, LeaderboardContexts] = UNSET
    highlighted_info: Union[Unset, InfoToHighlight] = UNSET
    priority: Union[Unset, int] = UNSET
    description: Union[None, Unset, str] = UNSET
    link_service: Union[None, Unset, str] = UNSET
    link_service_icon: Union[None, Unset, str] = UNSET
    link: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        pinned_contexts: Union[Unset, str] = UNSET
        if not isinstance(self.pinned_contexts, Unset):
            pinned_contexts = self.pinned_contexts.value

        highlighted_info: Union[Unset, str] = UNSET
        if not isinstance(self.highlighted_info, Unset):
            highlighted_info = self.highlighted_info.value

        priority = self.priority

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        link_service: Union[None, Unset, str]
        if isinstance(self.link_service, Unset):
            link_service = UNSET
        else:
            link_service = self.link_service

        link_service_icon: Union[None, Unset, str]
        if isinstance(self.link_service_icon, Unset):
            link_service_icon = UNSET
        else:
            link_service_icon = self.link_service_icon

        link: Union[None, Unset, str]
        if isinstance(self.link, Unset):
            link = UNSET
        else:
            link = self.link

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if pinned_contexts is not UNSET:
            field_dict["pinnedContexts"] = pinned_contexts
        if highlighted_info is not UNSET:
            field_dict["highlightedInfo"] = highlighted_info
        if priority is not UNSET:
            field_dict["priority"] = priority
        if description is not UNSET:
            field_dict["description"] = description
        if link_service is not UNSET:
            field_dict["linkService"] = link_service
        if link_service_icon is not UNSET:
            field_dict["linkServiceIcon"] = link_service_icon
        if link is not UNSET:
            field_dict["link"] = link

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _pinned_contexts = d.pop("pinnedContexts", UNSET)
        pinned_contexts: Union[Unset, LeaderboardContexts]
        if isinstance(_pinned_contexts, Unset):
            pinned_contexts = UNSET
        else:
            pinned_contexts = LeaderboardContexts(_pinned_contexts)

        _highlighted_info = d.pop("highlightedInfo", UNSET)
        highlighted_info: Union[Unset, InfoToHighlight]
        if isinstance(_highlighted_info, Unset):
            highlighted_info = UNSET
        else:
            highlighted_info = InfoToHighlight(_highlighted_info)

        priority = d.pop("priority", UNSET)

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_link_service(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        link_service = _parse_link_service(d.pop("linkService", UNSET))

        def _parse_link_service_icon(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        link_service_icon = _parse_link_service_icon(d.pop("linkServiceIcon", UNSET))

        def _parse_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        link = _parse_link(d.pop("link", UNSET))

        score_metadata = cls(
            id=id,
            pinned_contexts=pinned_contexts,
            highlighted_info=highlighted_info,
            priority=priority,
            description=description,
            link_service=link_service,
            link_service_icon=link_service_icon,
            link=link,
        )

        return score_metadata
