from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="LegacyModifiers")


@_attrs_define
class LegacyModifiers:
    """
    Attributes:
        da (Union[Unset, float]): Dissapearing arrows
        fs (Union[Unset, float]): Faster song
        ss (Union[Unset, float]): Slower song
        sf (Union[Unset, float]): Super fast song
        gn (Union[Unset, float]): Ghost notes
        na (Union[Unset, float]): No arrows
        nb (Union[Unset, float]): No bombs
        nf (Union[Unset, float]): No fail
        no (Union[Unset, float]): No walls
        pm (Union[Unset, float]): Pro mode
        sc (Union[Unset, float]): Smaller notes
    """

    da: Union[Unset, float] = UNSET
    fs: Union[Unset, float] = UNSET
    ss: Union[Unset, float] = UNSET
    sf: Union[Unset, float] = UNSET
    gn: Union[Unset, float] = UNSET
    na: Union[Unset, float] = UNSET
    nb: Union[Unset, float] = UNSET
    nf: Union[Unset, float] = UNSET
    no: Union[Unset, float] = UNSET
    pm: Union[Unset, float] = UNSET
    sc: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        da = self.da

        fs = self.fs

        ss = self.ss

        sf = self.sf

        gn = self.gn

        na = self.na

        nb = self.nb

        nf = self.nf

        no = self.no

        pm = self.pm

        sc = self.sc

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if da is not UNSET:
            field_dict["da"] = da
        if fs is not UNSET:
            field_dict["fs"] = fs
        if ss is not UNSET:
            field_dict["ss"] = ss
        if sf is not UNSET:
            field_dict["sf"] = sf
        if gn is not UNSET:
            field_dict["gn"] = gn
        if na is not UNSET:
            field_dict["na"] = na
        if nb is not UNSET:
            field_dict["nb"] = nb
        if nf is not UNSET:
            field_dict["nf"] = nf
        if no is not UNSET:
            field_dict["no"] = no
        if pm is not UNSET:
            field_dict["pm"] = pm
        if sc is not UNSET:
            field_dict["sc"] = sc

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        da = d.pop("da", UNSET)

        fs = d.pop("fs", UNSET)

        ss = d.pop("ss", UNSET)

        sf = d.pop("sf", UNSET)

        gn = d.pop("gn", UNSET)

        na = d.pop("na", UNSET)

        nb = d.pop("nb", UNSET)

        nf = d.pop("nf", UNSET)

        no = d.pop("no", UNSET)

        pm = d.pop("pm", UNSET)

        sc = d.pop("sc", UNSET)

        legacy_modifiers = cls(
            da=da,
            fs=fs,
            ss=ss,
            sf=sf,
            gn=gn,
            na=na,
            nb=nb,
            nf=nf,
            no=no,
            pm=pm,
            sc=sc,
        )

        return legacy_modifiers
