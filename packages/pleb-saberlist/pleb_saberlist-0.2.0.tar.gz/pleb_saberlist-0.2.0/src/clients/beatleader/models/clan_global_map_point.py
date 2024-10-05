from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.clan_map_connection import ClanMapConnection


T = TypeVar("T", bound="ClanGlobalMapPoint")


@_attrs_define
class ClanGlobalMapPoint:
    """
    Attributes:
        leaderboard_id (Union[None, Unset, str]):
        cover_image (Union[None, Unset, str]):
        stars (Union[None, Unset, float]):
        tie (Union[Unset, bool]):
        clans (Union[List['ClanMapConnection'], None, Unset]):
    """

    leaderboard_id: Union[None, Unset, str] = UNSET
    cover_image: Union[None, Unset, str] = UNSET
    stars: Union[None, Unset, float] = UNSET
    tie: Union[Unset, bool] = UNSET
    clans: Union[List["ClanMapConnection"], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        leaderboard_id: Union[None, Unset, str]
        if isinstance(self.leaderboard_id, Unset):
            leaderboard_id = UNSET
        else:
            leaderboard_id = self.leaderboard_id

        cover_image: Union[None, Unset, str]
        if isinstance(self.cover_image, Unset):
            cover_image = UNSET
        else:
            cover_image = self.cover_image

        stars: Union[None, Unset, float]
        if isinstance(self.stars, Unset):
            stars = UNSET
        else:
            stars = self.stars

        tie = self.tie

        clans: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.clans, Unset):
            clans = UNSET
        elif isinstance(self.clans, list):
            clans = []
            for clans_type_0_item_data in self.clans:
                clans_type_0_item = clans_type_0_item_data.to_dict()
                clans.append(clans_type_0_item)

        else:
            clans = self.clans

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if leaderboard_id is not UNSET:
            field_dict["leaderboardId"] = leaderboard_id
        if cover_image is not UNSET:
            field_dict["coverImage"] = cover_image
        if stars is not UNSET:
            field_dict["stars"] = stars
        if tie is not UNSET:
            field_dict["tie"] = tie
        if clans is not UNSET:
            field_dict["clans"] = clans

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.clan_map_connection import ClanMapConnection

        d = src_dict.copy()

        def _parse_leaderboard_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        leaderboard_id = _parse_leaderboard_id(d.pop("leaderboardId", UNSET))

        def _parse_cover_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cover_image = _parse_cover_image(d.pop("coverImage", UNSET))

        def _parse_stars(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        stars = _parse_stars(d.pop("stars", UNSET))

        tie = d.pop("tie", UNSET)

        def _parse_clans(data: object) -> Union[List["ClanMapConnection"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                clans_type_0 = []
                _clans_type_0 = data
                for clans_type_0_item_data in _clans_type_0:
                    clans_type_0_item = ClanMapConnection.from_dict(clans_type_0_item_data)

                    clans_type_0.append(clans_type_0_item)

                return clans_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ClanMapConnection"], None, Unset], data)

        clans = _parse_clans(d.pop("clans", UNSET))

        clan_global_map_point = cls(
            leaderboard_id=leaderboard_id,
            cover_image=cover_image,
            stars=stars,
            tie=tie,
            clans=clans,
        )

        return clan_global_map_point
