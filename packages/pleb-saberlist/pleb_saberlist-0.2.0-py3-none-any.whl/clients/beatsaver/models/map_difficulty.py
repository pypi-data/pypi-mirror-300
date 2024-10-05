from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.map_difficulty_characteristic import MapDifficultyCharacteristic
from ..models.map_difficulty_difficulty import MapDifficultyDifficulty
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.map_parity_summary import MapParitySummary


T = TypeVar("T", bound="MapDifficulty")


@_attrs_define
class MapDifficulty:
    """
    Attributes:
        bl_stars (Union[Unset, Any]):
        bombs (Union[Unset, int]):
        characteristic (Union[Unset, MapDifficultyCharacteristic]):
        chroma (Union[Unset, bool]):
        cinema (Union[Unset, bool]):
        difficulty (Union[Unset, MapDifficultyDifficulty]):
        events (Union[Unset, int]):
        label (Union[Unset, str]):
        length (Union[Unset, float]):
        max_score (Union[Unset, int]):
        me (Union[Unset, bool]):
        ne (Union[Unset, bool]):
        njs (Union[Unset, Any]):
        notes (Union[Unset, int]):
        nps (Union[Unset, float]):
        obstacles (Union[Unset, int]):
        offset (Union[Unset, Any]):
        parity_summary (Union[Unset, MapParitySummary]):
        seconds (Union[Unset, float]):
        stars (Union[Unset, Any]):
    """

    bl_stars: Union[Unset, Any] = UNSET
    bombs: Union[Unset, int] = UNSET
    characteristic: Union[Unset, MapDifficultyCharacteristic] = UNSET
    chroma: Union[Unset, bool] = UNSET
    cinema: Union[Unset, bool] = UNSET
    difficulty: Union[Unset, MapDifficultyDifficulty] = UNSET
    events: Union[Unset, int] = UNSET
    label: Union[Unset, str] = UNSET
    length: Union[Unset, float] = UNSET
    max_score: Union[Unset, int] = UNSET
    me: Union[Unset, bool] = UNSET
    ne: Union[Unset, bool] = UNSET
    njs: Union[Unset, Any] = UNSET
    notes: Union[Unset, int] = UNSET
    nps: Union[Unset, float] = UNSET
    obstacles: Union[Unset, int] = UNSET
    offset: Union[Unset, Any] = UNSET
    parity_summary: Union[Unset, "MapParitySummary"] = UNSET
    seconds: Union[Unset, float] = UNSET
    stars: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bl_stars = self.bl_stars

        bombs = self.bombs

        characteristic: Union[Unset, str] = UNSET
        if not isinstance(self.characteristic, Unset):
            characteristic = self.characteristic.value

        chroma = self.chroma

        cinema = self.cinema

        difficulty: Union[Unset, str] = UNSET
        if not isinstance(self.difficulty, Unset):
            difficulty = self.difficulty.value

        events = self.events

        label = self.label

        length = self.length

        max_score = self.max_score

        me = self.me

        ne = self.ne

        njs = self.njs

        notes = self.notes

        nps = self.nps

        obstacles = self.obstacles

        offset = self.offset

        parity_summary: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parity_summary, Unset):
            parity_summary = self.parity_summary.to_dict()

        seconds = self.seconds

        stars = self.stars

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bl_stars is not UNSET:
            field_dict["blStars"] = bl_stars
        if bombs is not UNSET:
            field_dict["bombs"] = bombs
        if characteristic is not UNSET:
            field_dict["characteristic"] = characteristic
        if chroma is not UNSET:
            field_dict["chroma"] = chroma
        if cinema is not UNSET:
            field_dict["cinema"] = cinema
        if difficulty is not UNSET:
            field_dict["difficulty"] = difficulty
        if events is not UNSET:
            field_dict["events"] = events
        if label is not UNSET:
            field_dict["label"] = label
        if length is not UNSET:
            field_dict["length"] = length
        if max_score is not UNSET:
            field_dict["maxScore"] = max_score
        if me is not UNSET:
            field_dict["me"] = me
        if ne is not UNSET:
            field_dict["ne"] = ne
        if njs is not UNSET:
            field_dict["njs"] = njs
        if notes is not UNSET:
            field_dict["notes"] = notes
        if nps is not UNSET:
            field_dict["nps"] = nps
        if obstacles is not UNSET:
            field_dict["obstacles"] = obstacles
        if offset is not UNSET:
            field_dict["offset"] = offset
        if parity_summary is not UNSET:
            field_dict["paritySummary"] = parity_summary
        if seconds is not UNSET:
            field_dict["seconds"] = seconds
        if stars is not UNSET:
            field_dict["stars"] = stars

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.map_parity_summary import MapParitySummary

        d = src_dict.copy()
        bl_stars = d.pop("blStars", UNSET)

        bombs = d.pop("bombs", UNSET)

        _characteristic = d.pop("characteristic", UNSET)
        characteristic: Union[Unset, MapDifficultyCharacteristic]
        if isinstance(_characteristic, Unset):
            characteristic = UNSET
        else:
            characteristic = MapDifficultyCharacteristic(_characteristic)

        chroma = d.pop("chroma", UNSET)

        cinema = d.pop("cinema", UNSET)

        _difficulty = d.pop("difficulty", UNSET)
        difficulty: Union[Unset, MapDifficultyDifficulty]
        if isinstance(_difficulty, Unset):
            difficulty = UNSET
        else:
            difficulty = MapDifficultyDifficulty(_difficulty)

        events = d.pop("events", UNSET)

        label = d.pop("label", UNSET)

        length = d.pop("length", UNSET)

        max_score = d.pop("maxScore", UNSET)

        me = d.pop("me", UNSET)

        ne = d.pop("ne", UNSET)

        njs = d.pop("njs", UNSET)

        notes = d.pop("notes", UNSET)

        nps = d.pop("nps", UNSET)

        obstacles = d.pop("obstacles", UNSET)

        offset = d.pop("offset", UNSET)

        _parity_summary = d.pop("paritySummary", UNSET)
        parity_summary: Union[Unset, MapParitySummary]
        if isinstance(_parity_summary, Unset):
            parity_summary = UNSET
        else:
            parity_summary = MapParitySummary.from_dict(_parity_summary)

        seconds = d.pop("seconds", UNSET)

        stars = d.pop("stars", UNSET)

        map_difficulty = cls(
            bl_stars=bl_stars,
            bombs=bombs,
            characteristic=characteristic,
            chroma=chroma,
            cinema=cinema,
            difficulty=difficulty,
            events=events,
            label=label,
            length=length,
            max_score=max_score,
            me=me,
            ne=ne,
            njs=njs,
            notes=notes,
            nps=nps,
            obstacles=obstacles,
            offset=offset,
            parity_summary=parity_summary,
            seconds=seconds,
            stars=stars,
        )

        map_difficulty.additional_properties = d
        return map_difficulty

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
