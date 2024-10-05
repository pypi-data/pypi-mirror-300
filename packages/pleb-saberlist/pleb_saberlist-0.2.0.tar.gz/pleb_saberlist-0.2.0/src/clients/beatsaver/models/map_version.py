import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.map_version_state import MapVersionState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.map_difficulty import MapDifficulty
    from ..models.map_testplay import MapTestplay


T = TypeVar("T", bound="MapVersion")


@_attrs_define
class MapVersion:
    """
    Attributes:
        cover_url (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        diffs (Union[Unset, List['MapDifficulty']]):
        download_url (Union[Unset, str]):
        feedback (Union[Unset, str]):
        hash_ (Union[Unset, str]):
        key (Union[Unset, str]):
        preview_url (Union[Unset, str]):
        sage_score (Union[Unset, Any]):
        scheduled_at (Union[Unset, datetime.datetime]):
        state (Union[Unset, MapVersionState]):
        testplay_at (Union[Unset, datetime.datetime]):
        testplays (Union[Unset, List['MapTestplay']]):
    """

    cover_url: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    diffs: Union[Unset, List["MapDifficulty"]] = UNSET
    download_url: Union[Unset, str] = UNSET
    feedback: Union[Unset, str] = UNSET
    hash_: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    preview_url: Union[Unset, str] = UNSET
    sage_score: Union[Unset, Any] = UNSET
    scheduled_at: Union[Unset, datetime.datetime] = UNSET
    state: Union[Unset, MapVersionState] = UNSET
    testplay_at: Union[Unset, datetime.datetime] = UNSET
    testplays: Union[Unset, List["MapTestplay"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cover_url = self.cover_url

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        diffs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.diffs, Unset):
            diffs = []
            for diffs_item_data in self.diffs:
                diffs_item = diffs_item_data.to_dict()
                diffs.append(diffs_item)

        download_url = self.download_url

        feedback = self.feedback

        hash_ = self.hash_

        key = self.key

        preview_url = self.preview_url

        sage_score = self.sage_score

        scheduled_at: Union[Unset, str] = UNSET
        if not isinstance(self.scheduled_at, Unset):
            scheduled_at = self.scheduled_at.isoformat()

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        testplay_at: Union[Unset, str] = UNSET
        if not isinstance(self.testplay_at, Unset):
            testplay_at = self.testplay_at.isoformat()

        testplays: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.testplays, Unset):
            testplays = []
            for testplays_item_data in self.testplays:
                testplays_item = testplays_item_data.to_dict()
                testplays.append(testplays_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cover_url is not UNSET:
            field_dict["coverURL"] = cover_url
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if diffs is not UNSET:
            field_dict["diffs"] = diffs
        if download_url is not UNSET:
            field_dict["downloadURL"] = download_url
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if hash_ is not UNSET:
            field_dict["hash"] = hash_
        if key is not UNSET:
            field_dict["key"] = key
        if preview_url is not UNSET:
            field_dict["previewURL"] = preview_url
        if sage_score is not UNSET:
            field_dict["sageScore"] = sage_score
        if scheduled_at is not UNSET:
            field_dict["scheduledAt"] = scheduled_at
        if state is not UNSET:
            field_dict["state"] = state
        if testplay_at is not UNSET:
            field_dict["testplayAt"] = testplay_at
        if testplays is not UNSET:
            field_dict["testplays"] = testplays

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.map_difficulty import MapDifficulty
        from ..models.map_testplay import MapTestplay

        d = src_dict.copy()
        cover_url = d.pop("coverURL", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        diffs = []
        _diffs = d.pop("diffs", UNSET)
        for diffs_item_data in _diffs or []:
            diffs_item = MapDifficulty.from_dict(diffs_item_data)

            diffs.append(diffs_item)

        download_url = d.pop("downloadURL", UNSET)

        feedback = d.pop("feedback", UNSET)

        hash_ = d.pop("hash", UNSET)

        key = d.pop("key", UNSET)

        preview_url = d.pop("previewURL", UNSET)

        sage_score = d.pop("sageScore", UNSET)

        _scheduled_at = d.pop("scheduledAt", UNSET)
        scheduled_at: Union[Unset, datetime.datetime]
        if isinstance(_scheduled_at, Unset):
            scheduled_at = UNSET
        else:
            scheduled_at = isoparse(_scheduled_at)

        _state = d.pop("state", UNSET)
        state: Union[Unset, MapVersionState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = MapVersionState(_state)

        _testplay_at = d.pop("testplayAt", UNSET)
        testplay_at: Union[Unset, datetime.datetime]
        if isinstance(_testplay_at, Unset):
            testplay_at = UNSET
        else:
            testplay_at = isoparse(_testplay_at)

        testplays = []
        _testplays = d.pop("testplays", UNSET)
        for testplays_item_data in _testplays or []:
            testplays_item = MapTestplay.from_dict(testplays_item_data)

            testplays.append(testplays_item)

        map_version = cls(
            cover_url=cover_url,
            created_at=created_at,
            diffs=diffs,
            download_url=download_url,
            feedback=feedback,
            hash_=hash_,
            key=key,
            preview_url=preview_url,
            sage_score=sage_score,
            scheduled_at=scheduled_at,
            state=state,
            testplay_at=testplay_at,
            testplays=testplays,
        )

        map_version.additional_properties = d
        return map_version

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
