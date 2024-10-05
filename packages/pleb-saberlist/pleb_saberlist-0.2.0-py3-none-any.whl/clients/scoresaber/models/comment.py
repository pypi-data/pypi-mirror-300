from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="Comment")


@_attrs_define
class Comment:
    """
    Attributes:
        username (str):
        user_id (str):
        comment (str):
        time_stamp (str):
    """

    username: str
    user_id: str
    comment: str
    time_stamp: str

    def to_dict(self) -> Dict[str, Any]:
        username = self.username

        user_id = self.user_id

        comment = self.comment

        time_stamp = self.time_stamp

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "username": username,
                "userId": user_id,
                "comment": comment,
                "timeStamp": time_stamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username")

        user_id = d.pop("userId")

        comment = d.pop("comment")

        time_stamp = d.pop("timeStamp")

        comment = cls(
            username=username,
            user_id=user_id,
            comment=comment,
            time_stamp=time_stamp,
        )

        return comment
