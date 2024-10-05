from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.song_status import SongStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExternalStatus")


@_attrs_define
class ExternalStatus:
    """
    Attributes:
        id (Union[Unset, int]):
        status (Union[Unset, SongStatus]):
        timeset (Union[Unset, int]):
        link (Union[None, Unset, str]):
        responsible (Union[None, Unset, str]):
        details (Union[None, Unset, str]):
        title (Union[None, Unset, str]):
        title_color (Union[None, Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    status: Union[Unset, SongStatus] = UNSET
    timeset: Union[Unset, int] = UNSET
    link: Union[None, Unset, str] = UNSET
    responsible: Union[None, Unset, str] = UNSET
    details: Union[None, Unset, str] = UNSET
    title: Union[None, Unset, str] = UNSET
    title_color: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        timeset = self.timeset

        link: Union[None, Unset, str]
        if isinstance(self.link, Unset):
            link = UNSET
        else:
            link = self.link

        responsible: Union[None, Unset, str]
        if isinstance(self.responsible, Unset):
            responsible = UNSET
        else:
            responsible = self.responsible

        details: Union[None, Unset, str]
        if isinstance(self.details, Unset):
            details = UNSET
        else:
            details = self.details

        title: Union[None, Unset, str]
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        title_color: Union[None, Unset, str]
        if isinstance(self.title_color, Unset):
            title_color = UNSET
        else:
            title_color = self.title_color

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status
        if timeset is not UNSET:
            field_dict["timeset"] = timeset
        if link is not UNSET:
            field_dict["link"] = link
        if responsible is not UNSET:
            field_dict["responsible"] = responsible
        if details is not UNSET:
            field_dict["details"] = details
        if title is not UNSET:
            field_dict["title"] = title
        if title_color is not UNSET:
            field_dict["titleColor"] = title_color

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, SongStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = SongStatus(_status)

        timeset = d.pop("timeset", UNSET)

        def _parse_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        link = _parse_link(d.pop("link", UNSET))

        def _parse_responsible(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        responsible = _parse_responsible(d.pop("responsible", UNSET))

        def _parse_details(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        details = _parse_details(d.pop("details", UNSET))

        def _parse_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_title_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title_color = _parse_title_color(d.pop("titleColor", UNSET))

        external_status = cls(
            id=id,
            status=status,
            timeset=timeset,
            link=link,
            responsible=responsible,
            details=details,
            title=title,
            title_color=title_color,
        )

        return external_status
