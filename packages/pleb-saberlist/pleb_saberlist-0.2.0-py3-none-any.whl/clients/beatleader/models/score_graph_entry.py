from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScoreGraphEntry")


@_attrs_define
class ScoreGraphEntry:
    """
    Attributes:
        player_id (Union[None, Unset, str]):
        weight (Union[Unset, float]):
        rank (Union[Unset, int]):
        timepost (Union[Unset, int]):
        pauses (Union[Unset, int]):
        max_streak (Union[None, Unset, int]):
        mistakes (Union[Unset, int]):
        modifiers (Union[None, Unset, str]):
        player_rank (Union[Unset, int]):
        player_name (Union[None, Unset, str]):
        player_avatar (Union[None, Unset, str]):
        player_alias (Union[None, Unset, str]):
        accuracy (Union[Unset, float]):
        pp (Union[Unset, float]):
    """

    player_id: Union[None, Unset, str] = UNSET
    weight: Union[Unset, float] = UNSET
    rank: Union[Unset, int] = UNSET
    timepost: Union[Unset, int] = UNSET
    pauses: Union[Unset, int] = UNSET
    max_streak: Union[None, Unset, int] = UNSET
    mistakes: Union[Unset, int] = UNSET
    modifiers: Union[None, Unset, str] = UNSET
    player_rank: Union[Unset, int] = UNSET
    player_name: Union[None, Unset, str] = UNSET
    player_avatar: Union[None, Unset, str] = UNSET
    player_alias: Union[None, Unset, str] = UNSET
    accuracy: Union[Unset, float] = UNSET
    pp: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        player_id: Union[None, Unset, str]
        if isinstance(self.player_id, Unset):
            player_id = UNSET
        else:
            player_id = self.player_id

        weight = self.weight

        rank = self.rank

        timepost = self.timepost

        pauses = self.pauses

        max_streak: Union[None, Unset, int]
        if isinstance(self.max_streak, Unset):
            max_streak = UNSET
        else:
            max_streak = self.max_streak

        mistakes = self.mistakes

        modifiers: Union[None, Unset, str]
        if isinstance(self.modifiers, Unset):
            modifiers = UNSET
        else:
            modifiers = self.modifiers

        player_rank = self.player_rank

        player_name: Union[None, Unset, str]
        if isinstance(self.player_name, Unset):
            player_name = UNSET
        else:
            player_name = self.player_name

        player_avatar: Union[None, Unset, str]
        if isinstance(self.player_avatar, Unset):
            player_avatar = UNSET
        else:
            player_avatar = self.player_avatar

        player_alias: Union[None, Unset, str]
        if isinstance(self.player_alias, Unset):
            player_alias = UNSET
        else:
            player_alias = self.player_alias

        accuracy = self.accuracy

        pp = self.pp

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if player_id is not UNSET:
            field_dict["playerId"] = player_id
        if weight is not UNSET:
            field_dict["weight"] = weight
        if rank is not UNSET:
            field_dict["rank"] = rank
        if timepost is not UNSET:
            field_dict["timepost"] = timepost
        if pauses is not UNSET:
            field_dict["pauses"] = pauses
        if max_streak is not UNSET:
            field_dict["maxStreak"] = max_streak
        if mistakes is not UNSET:
            field_dict["mistakes"] = mistakes
        if modifiers is not UNSET:
            field_dict["modifiers"] = modifiers
        if player_rank is not UNSET:
            field_dict["playerRank"] = player_rank
        if player_name is not UNSET:
            field_dict["playerName"] = player_name
        if player_avatar is not UNSET:
            field_dict["playerAvatar"] = player_avatar
        if player_alias is not UNSET:
            field_dict["playerAlias"] = player_alias
        if accuracy is not UNSET:
            field_dict["accuracy"] = accuracy
        if pp is not UNSET:
            field_dict["pp"] = pp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_player_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_id = _parse_player_id(d.pop("playerId", UNSET))

        weight = d.pop("weight", UNSET)

        rank = d.pop("rank", UNSET)

        timepost = d.pop("timepost", UNSET)

        pauses = d.pop("pauses", UNSET)

        def _parse_max_streak(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_streak = _parse_max_streak(d.pop("maxStreak", UNSET))

        mistakes = d.pop("mistakes", UNSET)

        def _parse_modifiers(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        modifiers = _parse_modifiers(d.pop("modifiers", UNSET))

        player_rank = d.pop("playerRank", UNSET)

        def _parse_player_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_name = _parse_player_name(d.pop("playerName", UNSET))

        def _parse_player_avatar(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_avatar = _parse_player_avatar(d.pop("playerAvatar", UNSET))

        def _parse_player_alias(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        player_alias = _parse_player_alias(d.pop("playerAlias", UNSET))

        accuracy = d.pop("accuracy", UNSET)

        pp = d.pop("pp", UNSET)

        score_graph_entry = cls(
            player_id=player_id,
            weight=weight,
            rank=rank,
            timepost=timepost,
            pauses=pauses,
            max_streak=max_streak,
            mistakes=mistakes,
            modifiers=modifiers,
            player_rank=player_rank,
            player_name=player_name,
            player_avatar=player_avatar,
            player_alias=player_alias,
            accuracy=accuracy,
            pp=pp,
        )

        return score_graph_entry
