from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModifiersRating")


@_attrs_define
class ModifiersRating:
    """
    Attributes:
        id (Union[Unset, int]):
        ss_predicted_acc (Union[Unset, float]):
        ss_pass_rating (Union[Unset, float]):
        ss_acc_rating (Union[Unset, float]):
        ss_tech_rating (Union[Unset, float]):
        ss_stars (Union[Unset, float]):
        fs_predicted_acc (Union[Unset, float]):
        fs_pass_rating (Union[Unset, float]):
        fs_acc_rating (Union[Unset, float]):
        fs_tech_rating (Union[Unset, float]):
        fs_stars (Union[Unset, float]):
        sf_predicted_acc (Union[Unset, float]):
        sf_pass_rating (Union[Unset, float]):
        sf_acc_rating (Union[Unset, float]):
        sf_tech_rating (Union[Unset, float]):
        sf_stars (Union[Unset, float]):
        bfs_predicted_acc (Union[Unset, float]):
        bfs_pass_rating (Union[Unset, float]):
        bfs_acc_rating (Union[Unset, float]):
        bfs_tech_rating (Union[Unset, float]):
        bfs_stars (Union[Unset, float]):
        bsf_predicted_acc (Union[Unset, float]):
        bsf_pass_rating (Union[Unset, float]):
        bsf_acc_rating (Union[Unset, float]):
        bsf_tech_rating (Union[Unset, float]):
        bsf_stars (Union[Unset, float]):
    """

    id: Union[Unset, int] = UNSET
    ss_predicted_acc: Union[Unset, float] = UNSET
    ss_pass_rating: Union[Unset, float] = UNSET
    ss_acc_rating: Union[Unset, float] = UNSET
    ss_tech_rating: Union[Unset, float] = UNSET
    ss_stars: Union[Unset, float] = UNSET
    fs_predicted_acc: Union[Unset, float] = UNSET
    fs_pass_rating: Union[Unset, float] = UNSET
    fs_acc_rating: Union[Unset, float] = UNSET
    fs_tech_rating: Union[Unset, float] = UNSET
    fs_stars: Union[Unset, float] = UNSET
    sf_predicted_acc: Union[Unset, float] = UNSET
    sf_pass_rating: Union[Unset, float] = UNSET
    sf_acc_rating: Union[Unset, float] = UNSET
    sf_tech_rating: Union[Unset, float] = UNSET
    sf_stars: Union[Unset, float] = UNSET
    bfs_predicted_acc: Union[Unset, float] = UNSET
    bfs_pass_rating: Union[Unset, float] = UNSET
    bfs_acc_rating: Union[Unset, float] = UNSET
    bfs_tech_rating: Union[Unset, float] = UNSET
    bfs_stars: Union[Unset, float] = UNSET
    bsf_predicted_acc: Union[Unset, float] = UNSET
    bsf_pass_rating: Union[Unset, float] = UNSET
    bsf_acc_rating: Union[Unset, float] = UNSET
    bsf_tech_rating: Union[Unset, float] = UNSET
    bsf_stars: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        ss_predicted_acc = self.ss_predicted_acc

        ss_pass_rating = self.ss_pass_rating

        ss_acc_rating = self.ss_acc_rating

        ss_tech_rating = self.ss_tech_rating

        ss_stars = self.ss_stars

        fs_predicted_acc = self.fs_predicted_acc

        fs_pass_rating = self.fs_pass_rating

        fs_acc_rating = self.fs_acc_rating

        fs_tech_rating = self.fs_tech_rating

        fs_stars = self.fs_stars

        sf_predicted_acc = self.sf_predicted_acc

        sf_pass_rating = self.sf_pass_rating

        sf_acc_rating = self.sf_acc_rating

        sf_tech_rating = self.sf_tech_rating

        sf_stars = self.sf_stars

        bfs_predicted_acc = self.bfs_predicted_acc

        bfs_pass_rating = self.bfs_pass_rating

        bfs_acc_rating = self.bfs_acc_rating

        bfs_tech_rating = self.bfs_tech_rating

        bfs_stars = self.bfs_stars

        bsf_predicted_acc = self.bsf_predicted_acc

        bsf_pass_rating = self.bsf_pass_rating

        bsf_acc_rating = self.bsf_acc_rating

        bsf_tech_rating = self.bsf_tech_rating

        bsf_stars = self.bsf_stars

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if ss_predicted_acc is not UNSET:
            field_dict["ssPredictedAcc"] = ss_predicted_acc
        if ss_pass_rating is not UNSET:
            field_dict["ssPassRating"] = ss_pass_rating
        if ss_acc_rating is not UNSET:
            field_dict["ssAccRating"] = ss_acc_rating
        if ss_tech_rating is not UNSET:
            field_dict["ssTechRating"] = ss_tech_rating
        if ss_stars is not UNSET:
            field_dict["ssStars"] = ss_stars
        if fs_predicted_acc is not UNSET:
            field_dict["fsPredictedAcc"] = fs_predicted_acc
        if fs_pass_rating is not UNSET:
            field_dict["fsPassRating"] = fs_pass_rating
        if fs_acc_rating is not UNSET:
            field_dict["fsAccRating"] = fs_acc_rating
        if fs_tech_rating is not UNSET:
            field_dict["fsTechRating"] = fs_tech_rating
        if fs_stars is not UNSET:
            field_dict["fsStars"] = fs_stars
        if sf_predicted_acc is not UNSET:
            field_dict["sfPredictedAcc"] = sf_predicted_acc
        if sf_pass_rating is not UNSET:
            field_dict["sfPassRating"] = sf_pass_rating
        if sf_acc_rating is not UNSET:
            field_dict["sfAccRating"] = sf_acc_rating
        if sf_tech_rating is not UNSET:
            field_dict["sfTechRating"] = sf_tech_rating
        if sf_stars is not UNSET:
            field_dict["sfStars"] = sf_stars
        if bfs_predicted_acc is not UNSET:
            field_dict["bfsPredictedAcc"] = bfs_predicted_acc
        if bfs_pass_rating is not UNSET:
            field_dict["bfsPassRating"] = bfs_pass_rating
        if bfs_acc_rating is not UNSET:
            field_dict["bfsAccRating"] = bfs_acc_rating
        if bfs_tech_rating is not UNSET:
            field_dict["bfsTechRating"] = bfs_tech_rating
        if bfs_stars is not UNSET:
            field_dict["bfsStars"] = bfs_stars
        if bsf_predicted_acc is not UNSET:
            field_dict["bsfPredictedAcc"] = bsf_predicted_acc
        if bsf_pass_rating is not UNSET:
            field_dict["bsfPassRating"] = bsf_pass_rating
        if bsf_acc_rating is not UNSET:
            field_dict["bsfAccRating"] = bsf_acc_rating
        if bsf_tech_rating is not UNSET:
            field_dict["bsfTechRating"] = bsf_tech_rating
        if bsf_stars is not UNSET:
            field_dict["bsfStars"] = bsf_stars

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        ss_predicted_acc = d.pop("ssPredictedAcc", UNSET)

        ss_pass_rating = d.pop("ssPassRating", UNSET)

        ss_acc_rating = d.pop("ssAccRating", UNSET)

        ss_tech_rating = d.pop("ssTechRating", UNSET)

        ss_stars = d.pop("ssStars", UNSET)

        fs_predicted_acc = d.pop("fsPredictedAcc", UNSET)

        fs_pass_rating = d.pop("fsPassRating", UNSET)

        fs_acc_rating = d.pop("fsAccRating", UNSET)

        fs_tech_rating = d.pop("fsTechRating", UNSET)

        fs_stars = d.pop("fsStars", UNSET)

        sf_predicted_acc = d.pop("sfPredictedAcc", UNSET)

        sf_pass_rating = d.pop("sfPassRating", UNSET)

        sf_acc_rating = d.pop("sfAccRating", UNSET)

        sf_tech_rating = d.pop("sfTechRating", UNSET)

        sf_stars = d.pop("sfStars", UNSET)

        bfs_predicted_acc = d.pop("bfsPredictedAcc", UNSET)

        bfs_pass_rating = d.pop("bfsPassRating", UNSET)

        bfs_acc_rating = d.pop("bfsAccRating", UNSET)

        bfs_tech_rating = d.pop("bfsTechRating", UNSET)

        bfs_stars = d.pop("bfsStars", UNSET)

        bsf_predicted_acc = d.pop("bsfPredictedAcc", UNSET)

        bsf_pass_rating = d.pop("bsfPassRating", UNSET)

        bsf_acc_rating = d.pop("bsfAccRating", UNSET)

        bsf_tech_rating = d.pop("bsfTechRating", UNSET)

        bsf_stars = d.pop("bsfStars", UNSET)

        modifiers_rating = cls(
            id=id,
            ss_predicted_acc=ss_predicted_acc,
            ss_pass_rating=ss_pass_rating,
            ss_acc_rating=ss_acc_rating,
            ss_tech_rating=ss_tech_rating,
            ss_stars=ss_stars,
            fs_predicted_acc=fs_predicted_acc,
            fs_pass_rating=fs_pass_rating,
            fs_acc_rating=fs_acc_rating,
            fs_tech_rating=fs_tech_rating,
            fs_stars=fs_stars,
            sf_predicted_acc=sf_predicted_acc,
            sf_pass_rating=sf_pass_rating,
            sf_acc_rating=sf_acc_rating,
            sf_tech_rating=sf_tech_rating,
            sf_stars=sf_stars,
            bfs_predicted_acc=bfs_predicted_acc,
            bfs_pass_rating=bfs_pass_rating,
            bfs_acc_rating=bfs_acc_rating,
            bfs_tech_rating=bfs_tech_rating,
            bfs_stars=bfs_stars,
            bsf_predicted_acc=bsf_predicted_acc,
            bsf_pass_rating=bsf_pass_rating,
            bsf_acc_rating=bsf_acc_rating,
            bsf_tech_rating=bsf_tech_rating,
            bsf_stars=bsf_stars,
        )

        return modifiers_rating
