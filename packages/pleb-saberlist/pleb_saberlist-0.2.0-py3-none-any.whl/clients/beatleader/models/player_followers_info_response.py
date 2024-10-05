from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlayerFollowersInfoResponse")


@_attrs_define
class PlayerFollowersInfoResponse:
    """
    Attributes:
        following_count (Union[None, Unset, int]):
        me_following (Union[Unset, bool]):
        following (Union[List[str], None, Unset]):
        followers_count (Union[None, Unset, int]):
        i_follow (Union[Unset, bool]):
        followers (Union[List[str], None, Unset]):
    """

    following_count: Union[None, Unset, int] = UNSET
    me_following: Union[Unset, bool] = UNSET
    following: Union[List[str], None, Unset] = UNSET
    followers_count: Union[None, Unset, int] = UNSET
    i_follow: Union[Unset, bool] = UNSET
    followers: Union[List[str], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        following_count: Union[None, Unset, int]
        if isinstance(self.following_count, Unset):
            following_count = UNSET
        else:
            following_count = self.following_count

        me_following = self.me_following

        following: Union[List[str], None, Unset]
        if isinstance(self.following, Unset):
            following = UNSET
        elif isinstance(self.following, list):
            following = self.following

        else:
            following = self.following

        followers_count: Union[None, Unset, int]
        if isinstance(self.followers_count, Unset):
            followers_count = UNSET
        else:
            followers_count = self.followers_count

        i_follow = self.i_follow

        followers: Union[List[str], None, Unset]
        if isinstance(self.followers, Unset):
            followers = UNSET
        elif isinstance(self.followers, list):
            followers = self.followers

        else:
            followers = self.followers

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if following_count is not UNSET:
            field_dict["followingCount"] = following_count
        if me_following is not UNSET:
            field_dict["meFollowing"] = me_following
        if following is not UNSET:
            field_dict["following"] = following
        if followers_count is not UNSET:
            field_dict["followersCount"] = followers_count
        if i_follow is not UNSET:
            field_dict["iFollow"] = i_follow
        if followers is not UNSET:
            field_dict["followers"] = followers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_following_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        following_count = _parse_following_count(d.pop("followingCount", UNSET))

        me_following = d.pop("meFollowing", UNSET)

        def _parse_following(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                following_type_0 = cast(List[str], data)

                return following_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        following = _parse_following(d.pop("following", UNSET))

        def _parse_followers_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        followers_count = _parse_followers_count(d.pop("followersCount", UNSET))

        i_follow = d.pop("iFollow", UNSET)

        def _parse_followers(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                followers_type_0 = cast(List[str], data)

                return followers_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        followers = _parse_followers(d.pop("followers", UNSET))

        player_followers_info_response = cls(
            following_count=following_count,
            me_following=me_following,
            following=following,
            followers_count=followers_count,
            i_follow=i_follow,
            followers=followers,
        )

        return player_followers_info_response
