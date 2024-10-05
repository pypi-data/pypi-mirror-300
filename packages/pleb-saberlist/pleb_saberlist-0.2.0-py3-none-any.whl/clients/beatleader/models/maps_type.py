from enum import Enum


class MapsType(str, Enum):
    ALL = "all"
    RANKED = "ranked"
    UNRANKED = "unranked"

    def __str__(self) -> str:
        return str(self.value)
