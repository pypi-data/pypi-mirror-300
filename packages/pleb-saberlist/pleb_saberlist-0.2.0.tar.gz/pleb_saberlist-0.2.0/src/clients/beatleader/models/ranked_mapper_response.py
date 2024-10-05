from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ranked_map import RankedMap


T = TypeVar("T", bound="RankedMapperResponse")


@_attrs_define
class RankedMapperResponse:
    """
    Attributes:
        players_count (Union[Unset, int]):
        total_pp (Union[Unset, float]):
        maps (Union[List['RankedMap'], None, Unset]):
        total_map_count (Union[Unset, int]):
    """

    players_count: Union[Unset, int] = UNSET
    total_pp: Union[Unset, float] = UNSET
    maps: Union[List["RankedMap"], None, Unset] = UNSET
    total_map_count: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        players_count = self.players_count

        total_pp = self.total_pp

        maps: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.maps, Unset):
            maps = UNSET
        elif isinstance(self.maps, list):
            maps = []
            for maps_type_0_item_data in self.maps:
                maps_type_0_item = maps_type_0_item_data.to_dict()
                maps.append(maps_type_0_item)

        else:
            maps = self.maps

        total_map_count = self.total_map_count

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if players_count is not UNSET:
            field_dict["playersCount"] = players_count
        if total_pp is not UNSET:
            field_dict["totalPp"] = total_pp
        if maps is not UNSET:
            field_dict["maps"] = maps
        if total_map_count is not UNSET:
            field_dict["totalMapCount"] = total_map_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ranked_map import RankedMap

        d = src_dict.copy()
        players_count = d.pop("playersCount", UNSET)

        total_pp = d.pop("totalPp", UNSET)

        def _parse_maps(data: object) -> Union[List["RankedMap"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                maps_type_0 = []
                _maps_type_0 = data
                for maps_type_0_item_data in _maps_type_0:
                    maps_type_0_item = RankedMap.from_dict(maps_type_0_item_data)

                    maps_type_0.append(maps_type_0_item)

                return maps_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["RankedMap"], None, Unset], data)

        maps = _parse_maps(d.pop("maps", UNSET))

        total_map_count = d.pop("totalMapCount", UNSET)

        ranked_mapper_response = cls(
            players_count=players_count,
            total_pp=total_pp,
            maps=maps,
            total_map_count=total_map_count,
        )

        return ranked_mapper_response
