from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProfileSettings")


@_attrs_define
class ProfileSettings:
    """
    Attributes:
        id (Union[Unset, int]):
        bio (Union[None, Unset, str]):
        message (Union[None, Unset, str]):
        effect_name (Union[None, Unset, str]):
        profile_appearance (Union[None, Unset, str]):
        hue (Union[None, Unset, float]):
        saturation (Union[None, Unset, float]):
        left_saber_color (Union[None, Unset, str]):
        right_saber_color (Union[None, Unset, str]):
        profile_cover (Union[None, Unset, str]):
        starred_friends (Union[None, Unset, str]):
        horizontal_rich_bio (Union[Unset, bool]):
        ranked_mapper_sort (Union[None, Unset, str]):
        show_bots (Union[Unset, bool]):
        show_all_ratings (Union[Unset, bool]):
        show_stats_public (Union[Unset, bool]):
        show_stats_public_pinned (Union[Unset, bool]):
    """

    id: Union[Unset, int] = UNSET
    bio: Union[None, Unset, str] = UNSET
    message: Union[None, Unset, str] = UNSET
    effect_name: Union[None, Unset, str] = UNSET
    profile_appearance: Union[None, Unset, str] = UNSET
    hue: Union[None, Unset, float] = UNSET
    saturation: Union[None, Unset, float] = UNSET
    left_saber_color: Union[None, Unset, str] = UNSET
    right_saber_color: Union[None, Unset, str] = UNSET
    profile_cover: Union[None, Unset, str] = UNSET
    starred_friends: Union[None, Unset, str] = UNSET
    horizontal_rich_bio: Union[Unset, bool] = UNSET
    ranked_mapper_sort: Union[None, Unset, str] = UNSET
    show_bots: Union[Unset, bool] = UNSET
    show_all_ratings: Union[Unset, bool] = UNSET
    show_stats_public: Union[Unset, bool] = UNSET
    show_stats_public_pinned: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        bio: Union[None, Unset, str]
        if isinstance(self.bio, Unset):
            bio = UNSET
        else:
            bio = self.bio

        message: Union[None, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        effect_name: Union[None, Unset, str]
        if isinstance(self.effect_name, Unset):
            effect_name = UNSET
        else:
            effect_name = self.effect_name

        profile_appearance: Union[None, Unset, str]
        if isinstance(self.profile_appearance, Unset):
            profile_appearance = UNSET
        else:
            profile_appearance = self.profile_appearance

        hue: Union[None, Unset, float]
        if isinstance(self.hue, Unset):
            hue = UNSET
        else:
            hue = self.hue

        saturation: Union[None, Unset, float]
        if isinstance(self.saturation, Unset):
            saturation = UNSET
        else:
            saturation = self.saturation

        left_saber_color: Union[None, Unset, str]
        if isinstance(self.left_saber_color, Unset):
            left_saber_color = UNSET
        else:
            left_saber_color = self.left_saber_color

        right_saber_color: Union[None, Unset, str]
        if isinstance(self.right_saber_color, Unset):
            right_saber_color = UNSET
        else:
            right_saber_color = self.right_saber_color

        profile_cover: Union[None, Unset, str]
        if isinstance(self.profile_cover, Unset):
            profile_cover = UNSET
        else:
            profile_cover = self.profile_cover

        starred_friends: Union[None, Unset, str]
        if isinstance(self.starred_friends, Unset):
            starred_friends = UNSET
        else:
            starred_friends = self.starred_friends

        horizontal_rich_bio = self.horizontal_rich_bio

        ranked_mapper_sort: Union[None, Unset, str]
        if isinstance(self.ranked_mapper_sort, Unset):
            ranked_mapper_sort = UNSET
        else:
            ranked_mapper_sort = self.ranked_mapper_sort

        show_bots = self.show_bots

        show_all_ratings = self.show_all_ratings

        show_stats_public = self.show_stats_public

        show_stats_public_pinned = self.show_stats_public_pinned

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if bio is not UNSET:
            field_dict["bio"] = bio
        if message is not UNSET:
            field_dict["message"] = message
        if effect_name is not UNSET:
            field_dict["effectName"] = effect_name
        if profile_appearance is not UNSET:
            field_dict["profileAppearance"] = profile_appearance
        if hue is not UNSET:
            field_dict["hue"] = hue
        if saturation is not UNSET:
            field_dict["saturation"] = saturation
        if left_saber_color is not UNSET:
            field_dict["leftSaberColor"] = left_saber_color
        if right_saber_color is not UNSET:
            field_dict["rightSaberColor"] = right_saber_color
        if profile_cover is not UNSET:
            field_dict["profileCover"] = profile_cover
        if starred_friends is not UNSET:
            field_dict["starredFriends"] = starred_friends
        if horizontal_rich_bio is not UNSET:
            field_dict["horizontalRichBio"] = horizontal_rich_bio
        if ranked_mapper_sort is not UNSET:
            field_dict["rankedMapperSort"] = ranked_mapper_sort
        if show_bots is not UNSET:
            field_dict["showBots"] = show_bots
        if show_all_ratings is not UNSET:
            field_dict["showAllRatings"] = show_all_ratings
        if show_stats_public is not UNSET:
            field_dict["showStatsPublic"] = show_stats_public
        if show_stats_public_pinned is not UNSET:
            field_dict["showStatsPublicPinned"] = show_stats_public_pinned

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_bio(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bio = _parse_bio(d.pop("bio", UNSET))

        def _parse_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_effect_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        effect_name = _parse_effect_name(d.pop("effectName", UNSET))

        def _parse_profile_appearance(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        profile_appearance = _parse_profile_appearance(d.pop("profileAppearance", UNSET))

        def _parse_hue(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        hue = _parse_hue(d.pop("hue", UNSET))

        def _parse_saturation(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        saturation = _parse_saturation(d.pop("saturation", UNSET))

        def _parse_left_saber_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        left_saber_color = _parse_left_saber_color(d.pop("leftSaberColor", UNSET))

        def _parse_right_saber_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        right_saber_color = _parse_right_saber_color(d.pop("rightSaberColor", UNSET))

        def _parse_profile_cover(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        profile_cover = _parse_profile_cover(d.pop("profileCover", UNSET))

        def _parse_starred_friends(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        starred_friends = _parse_starred_friends(d.pop("starredFriends", UNSET))

        horizontal_rich_bio = d.pop("horizontalRichBio", UNSET)

        def _parse_ranked_mapper_sort(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ranked_mapper_sort = _parse_ranked_mapper_sort(d.pop("rankedMapperSort", UNSET))

        show_bots = d.pop("showBots", UNSET)

        show_all_ratings = d.pop("showAllRatings", UNSET)

        show_stats_public = d.pop("showStatsPublic", UNSET)

        show_stats_public_pinned = d.pop("showStatsPublicPinned", UNSET)

        profile_settings = cls(
            id=id,
            bio=bio,
            message=message,
            effect_name=effect_name,
            profile_appearance=profile_appearance,
            hue=hue,
            saturation=saturation,
            left_saber_color=left_saber_color,
            right_saber_color=right_saber_color,
            profile_cover=profile_cover,
            starred_friends=starred_friends,
            horizontal_rich_bio=horizontal_rich_bio,
            ranked_mapper_sort=ranked_mapper_sort,
            show_bots=show_bots,
            show_all_ratings=show_all_ratings,
            show_stats_public=show_stats_public,
            show_stats_public_pinned=show_stats_public_pinned,
        )

        return profile_settings
