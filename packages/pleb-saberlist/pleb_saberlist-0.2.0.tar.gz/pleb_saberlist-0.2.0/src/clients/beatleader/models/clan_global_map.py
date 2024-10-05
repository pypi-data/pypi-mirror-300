from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.clan_global_map_point import ClanGlobalMapPoint
    from ..models.clan_point import ClanPoint


T = TypeVar("T", bound="ClanGlobalMap")


@_attrs_define
class ClanGlobalMap:
    """
    Attributes:
        points (Union[List['ClanGlobalMapPoint'], None, Unset]):
        clans (Union[List['ClanPoint'], None, Unset]):
    """

    points: Union[List["ClanGlobalMapPoint"], None, Unset] = UNSET
    clans: Union[List["ClanPoint"], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        points: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.points, Unset):
            points = UNSET
        elif isinstance(self.points, list):
            points = []
            for points_type_0_item_data in self.points:
                points_type_0_item = points_type_0_item_data.to_dict()
                points.append(points_type_0_item)

        else:
            points = self.points

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
        if points is not UNSET:
            field_dict["points"] = points
        if clans is not UNSET:
            field_dict["clans"] = clans

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.clan_global_map_point import ClanGlobalMapPoint
        from ..models.clan_point import ClanPoint

        d = src_dict.copy()

        def _parse_points(data: object) -> Union[List["ClanGlobalMapPoint"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                points_type_0 = []
                _points_type_0 = data
                for points_type_0_item_data in _points_type_0:
                    points_type_0_item = ClanGlobalMapPoint.from_dict(points_type_0_item_data)

                    points_type_0.append(points_type_0_item)

                return points_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ClanGlobalMapPoint"], None, Unset], data)

        points = _parse_points(d.pop("points", UNSET))

        def _parse_clans(data: object) -> Union[List["ClanPoint"], None, Unset]:
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
                    clans_type_0_item = ClanPoint.from_dict(clans_type_0_item_data)

                    clans_type_0.append(clans_type_0_item)

                return clans_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ClanPoint"], None, Unset], data)

        clans = _parse_clans(d.pop("clans", UNSET))

        clan_global_map = cls(
            points=points,
            clans=clans,
        )

        return clan_global_map
