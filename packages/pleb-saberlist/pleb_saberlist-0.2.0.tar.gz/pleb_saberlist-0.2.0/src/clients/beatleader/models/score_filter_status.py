from enum import Enum


class ScoreFilterStatus(str, Enum):
    NONE = "none"
    SUSPICIOUS = "suspicious"

    def __str__(self) -> str:
        return str(self.value)
