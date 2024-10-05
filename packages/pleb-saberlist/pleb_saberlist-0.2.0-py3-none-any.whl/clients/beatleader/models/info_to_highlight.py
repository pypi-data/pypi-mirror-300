from enum import Enum


class InfoToHighlight(str, Enum):
    NONE = "none"
    PLAYCOUNT = "playCount"
    WATCHCOUNT = "watchCount"

    def __str__(self) -> str:
        return str(self.value)
