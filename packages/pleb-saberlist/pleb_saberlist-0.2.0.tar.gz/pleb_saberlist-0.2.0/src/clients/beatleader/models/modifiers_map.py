from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModifiersMap")


@_attrs_define
class ModifiersMap:
    """
    Attributes:
        modifier_id (Union[Unset, int]):
        da (Union[Unset, float]):
        fs (Union[Unset, float]):
        sf (Union[Unset, float]):
        ss (Union[Unset, float]):
        gn (Union[Unset, float]):
        na (Union[Unset, float]):
        nb (Union[Unset, float]):
        nf (Union[Unset, float]):
        no (Union[Unset, float]):
        pm (Union[Unset, float]):
        sc (Union[Unset, float]):
        sa (Union[Unset, float]):
        op (Union[Unset, float]):
        ez (Union[Unset, float]):
        hd (Union[Unset, float]):
        smc (Union[Unset, float]):
        ohp (Union[Unset, float]):
    """

    modifier_id: Union[Unset, int] = UNSET
    da: Union[Unset, float] = UNSET
    fs: Union[Unset, float] = UNSET
    sf: Union[Unset, float] = UNSET
    ss: Union[Unset, float] = UNSET
    gn: Union[Unset, float] = UNSET
    na: Union[Unset, float] = UNSET
    nb: Union[Unset, float] = UNSET
    nf: Union[Unset, float] = UNSET
    no: Union[Unset, float] = UNSET
    pm: Union[Unset, float] = UNSET
    sc: Union[Unset, float] = UNSET
    sa: Union[Unset, float] = UNSET
    op: Union[Unset, float] = UNSET
    ez: Union[Unset, float] = UNSET
    hd: Union[Unset, float] = UNSET
    smc: Union[Unset, float] = UNSET
    ohp: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        modifier_id = self.modifier_id

        da = self.da

        fs = self.fs

        sf = self.sf

        ss = self.ss

        gn = self.gn

        na = self.na

        nb = self.nb

        nf = self.nf

        no = self.no

        pm = self.pm

        sc = self.sc

        sa = self.sa

        op = self.op

        ez = self.ez

        hd = self.hd

        smc = self.smc

        ohp = self.ohp

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if modifier_id is not UNSET:
            field_dict["modifierId"] = modifier_id
        if da is not UNSET:
            field_dict["da"] = da
        if fs is not UNSET:
            field_dict["fs"] = fs
        if sf is not UNSET:
            field_dict["sf"] = sf
        if ss is not UNSET:
            field_dict["ss"] = ss
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
        if sa is not UNSET:
            field_dict["sa"] = sa
        if op is not UNSET:
            field_dict["op"] = op
        if ez is not UNSET:
            field_dict["ez"] = ez
        if hd is not UNSET:
            field_dict["hd"] = hd
        if smc is not UNSET:
            field_dict["smc"] = smc
        if ohp is not UNSET:
            field_dict["ohp"] = ohp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        modifier_id = d.pop("modifierId", UNSET)

        da = d.pop("da", UNSET)

        fs = d.pop("fs", UNSET)

        sf = d.pop("sf", UNSET)

        ss = d.pop("ss", UNSET)

        gn = d.pop("gn", UNSET)

        na = d.pop("na", UNSET)

        nb = d.pop("nb", UNSET)

        nf = d.pop("nf", UNSET)

        no = d.pop("no", UNSET)

        pm = d.pop("pm", UNSET)

        sc = d.pop("sc", UNSET)

        sa = d.pop("sa", UNSET)

        op = d.pop("op", UNSET)

        ez = d.pop("ez", UNSET)

        hd = d.pop("hd", UNSET)

        smc = d.pop("smc", UNSET)

        ohp = d.pop("ohp", UNSET)

        modifiers_map = cls(
            modifier_id=modifier_id,
            da=da,
            fs=fs,
            sf=sf,
            ss=ss,
            gn=gn,
            na=na,
            nb=nb,
            nf=nf,
            no=no,
            pm=pm,
            sc=sc,
            sa=sa,
            op=op,
            ez=ez,
            hd=hd,
            smc=smc,
            ohp=ohp,
        )

        return modifiers_map
