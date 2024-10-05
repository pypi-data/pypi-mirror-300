from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.event_ranking import EventRanking


T = TypeVar("T", bound="EventPlayer")


@_attrs_define
class EventPlayer:
    """
    Attributes:
        id (Union[Unset, int]):
        event_ranking_id (Union[None, Unset, int]):
        event (Union[Unset, EventRanking]):
        event_name (Union[None, Unset, str]):
        player_name (Union[None, Unset, str]):
        player_id (Union[None, Unset, str]):
        country (Union[None, Unset, str]):
        rank (Union[Unset, int]):
        country_rank (Union[Unset, int]):
        pp (Union[Unset, float]):
    """

    id: Union[Unset, int] = UNSET
    event_ranking_id: Union[None, Unset, int] = UNSET
    event: Union[Unset, "EventRanking"] = UNSET
    event_name: Union[None, Unset, str] = UNSET
    player_name: Union[None, Unset, str] = UNSET
    player_id: Union[None, Unset, str] = UNSET
    country: Union[None, Unset, str] = UNSET
    rank: Union[Unset, int] = UNSET
    country_rank: Union[Unset, int] = UNSET
    pp: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        event_ranking_id: Union[None, Unset, int]
        if isinstance(self.event_ranking_id, Unset):
            event_ranking_id = UNSET
        else:
            event_ranking_id = self.event_ranking_id

        event: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.event, Unset):
            event = self.event.to_dict()

        event_name: Union[None, Unset, str]
        if isinstance(self.event_name, Unset):
            event_name = UNSET
        else:
            event_name = self.event_name

        player_name: Union[None, Unset, str]
        if isinstance(self.player_name, Unset):
            player_name = UNSET
        else:
            player_name = self.player_name

        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        country: Union[None, Unset, str]
        if isinstance(self.country, Unset):
            country = UNSET
        else:
            country = self.country

        rank = self.rank

        country_rank = self.country_rank

        pp = self.pp

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if event_ranking_id is not UNSET:
            field_dict["eventRankingId"] = event_ranking_id
        if event is not UNSET:
            field_dict["event"] = event
        if event_name is not UNSET:
            field_dict["eventName"] = event_name
        if player_name is not UNSET:
            field_dict["playerName"] = player_name
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if country is not UNSET:
            field_dict["country"] = country
        if rank is not UNSET:
            field_dict["rank"] = rank
        if country_rank is not UNSET:
            field_dict["countryRank"] = country_rank
        if pp is not UNSET:
            field_dict["pp"] = pp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.event_ranking import EventRanking

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_event_ranking_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        event_ranking_id = _parse_event_ranking_id(d.pop("eventRankingId", UNSET))

        _event = d.pop("event", UNSET)
        event: Union[Unset, EventRanking]
        if isinstance(_event, Unset):
            event = UNSET
        else:
            event = EventRanking.from_dict(_event)

        def _parse_event_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        event_name = _parse_event_name(d.pop("eventName", UNSET))

        def _parse_player_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_name = _parse_player_name(d.pop("playerName", UNSET))

        def _parse_player_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_id = _parse_player_id(d.pop("playerId", UNSET))

        def _parse_country(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        country = _parse_country(d.pop("country", UNSET))

        rank = d.pop("rank", UNSET)

        country_rank = d.pop("countryRank", UNSET)

        pp = d.pop("pp", UNSET)

        event_player = cls(
            id=id,
            event_ranking_id=event_ranking_id,
            event=event,
            event_name=event_name,
            player_name=player_name,
            player_id=player_id,
            country=country,
            rank=rank,
            country_rank=country_rank,
            pp=pp,
        )

        return event_player
