from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.clan import Clan


T = TypeVar("T", bound="GlobalMapHistory")


@_attrs_define
class GlobalMapHistory:
    """
    Attributes:
        id (Union[Unset, int]):
        timestamp (Union[Unset, int]):
        clan_id (Union[Unset, int]):
        clan (Union[Unset, Clan]):
        global_map_captured (Union[Unset, float]):
        players_count (Union[Unset, int]):
        pp (Union[Unset, float]):
        rank (Union[Unset, int]):
        average_rank (Union[Unset, float]):
        average_accuracy (Union[Unset, float]):
        capture_leaderboards_count (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    timestamp: Union[Unset, int] = UNSET
    clan_id: Union[Unset, int] = UNSET
    clan: Union[Unset, "Clan"] = UNSET
    global_map_captured: Union[Unset, float] = UNSET
    players_count: Union[Unset, int] = UNSET
    pp: Union[Unset, float] = UNSET
    rank: Union[Unset, int] = UNSET
    average_rank: Union[Unset, float] = UNSET
    average_accuracy: Union[Unset, float] = UNSET
    capture_leaderboards_count: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        timestamp = self.timestamp

        clan_id = self.clan_id

        clan: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.clan, Unset):
            clan = self.clan.to_dict()

        global_map_captured = self.global_map_captured

        players_count = self.players_count

        pp = self.pp

        rank = self.rank

        average_rank = self.average_rank

        average_accuracy = self.average_accuracy

        capture_leaderboards_count = self.capture_leaderboards_count

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if clan_id is not UNSET:
            field_dict["clanId"] = clan_id
        if clan is not UNSET:
            field_dict["clan"] = clan
        if global_map_captured is not UNSET:
            field_dict["globalMapCaptured"] = global_map_captured
        if players_count is not UNSET:
            field_dict["playersCount"] = players_count
        if pp is not UNSET:
            field_dict["pp"] = pp
        if rank is not UNSET:
            field_dict["rank"] = rank
        if average_rank is not UNSET:
            field_dict["averageRank"] = average_rank
        if average_accuracy is not UNSET:
            field_dict["averageAccuracy"] = average_accuracy
        if capture_leaderboards_count is not UNSET:
            field_dict["captureLeaderboardsCount"] = capture_leaderboards_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.clan import Clan

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        clan_id = d.pop("clanId", UNSET)

        _clan = d.pop("clan", UNSET)
        clan: Union[Unset, Clan]
        if isinstance(_clan, Unset):
            clan = UNSET
        else:
            clan = Clan.from_dict(_clan)

        global_map_captured = d.pop("globalMapCaptured", UNSET)

        players_count = d.pop("playersCount", UNSET)

        pp = d.pop("pp", UNSET)

        rank = d.pop("rank", UNSET)

        average_rank = d.pop("averageRank", UNSET)

        average_accuracy = d.pop("averageAccuracy", UNSET)

        capture_leaderboards_count = d.pop("captureLeaderboardsCount", UNSET)

        global_map_history = cls(
            id=id,
            timestamp=timestamp,
            clan_id=clan_id,
            clan=clan,
            global_map_captured=global_map_captured,
            players_count=players_count,
            pp=pp,
            rank=rank,
            average_rank=average_rank,
            average_accuracy=average_accuracy,
            capture_leaderboards_count=capture_leaderboards_count,
        )

        return global_map_history
