from enum import Enum


class FollowerType(str, Enum):
    FOLLOWERS = "followers"
    FOLLOWING = "following"

    def __str__(self) -> str:
        return str(self.value)
