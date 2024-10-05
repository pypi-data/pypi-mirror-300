from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.player_response_with_stats import PlayerResponseWithStats


T = TypeVar("T", bound="PlayerResponseWithStatsResponseWithMetadata")


@_attrs_define
class PlayerResponseWithStatsResponseWithMetadata:
    """
    Attributes:
        metadata (Union[Unset, Metadata]):
        data (Union[List['PlayerResponseWithStats'], None, Unset]):
    """

    metadata: Union[Unset, "Metadata"] = UNSET
    data: Union[List["PlayerResponseWithStats"], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        data: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.data, Unset):
            data = UNSET
        elif isinstance(self.data, list):
            data = []
            for data_type_0_item_data in self.data:
                data_type_0_item = data_type_0_item_data.to_dict()
                data.append(data_type_0_item)

        else:
            data = self.data

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metadata import Metadata
        from ..models.player_response_with_stats import PlayerResponseWithStats

        d = src_dict.copy()
        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, Metadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        def _parse_data(data: object) -> Union[List["PlayerResponseWithStats"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                data_type_0 = []
                _data_type_0 = data
                for data_type_0_item_data in _data_type_0:
                    data_type_0_item = PlayerResponseWithStats.from_dict(data_type_0_item_data)

                    data_type_0.append(data_type_0_item)

                return data_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["PlayerResponseWithStats"], None, Unset], data)

        data = _parse_data(d.pop("data", UNSET))

        player_response_with_stats_response_with_metadata = cls(
            metadata=metadata,
            data=data,
        )

        return player_response_with_stats_response_with_metadata
