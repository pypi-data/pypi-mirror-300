from enum import Enum


class GetApiPlayerPlayerIdScoresSort(str, Enum):
    RECENT = "recent"
    TOP = "top"

    def __str__(self) -> str:
        return str(self.value)
