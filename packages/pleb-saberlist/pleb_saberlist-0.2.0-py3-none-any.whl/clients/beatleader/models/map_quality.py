from enum import Enum


class MapQuality(str, Enum):
    BAD = "bad"
    GOOD = "good"
    OK = "ok"

    def __str__(self) -> str:
        return str(self.value)
