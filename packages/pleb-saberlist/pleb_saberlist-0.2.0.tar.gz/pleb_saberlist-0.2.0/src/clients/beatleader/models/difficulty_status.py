from enum import Enum


class DifficultyStatus(str, Enum):
    INEVENT = "inevent"
    NOMINATED = "nominated"
    OST = "oST"
    OUTDATED = "outdated"
    QUALIFIED = "qualified"
    RANKED = "ranked"
    UNRANKABLE = "unrankable"
    UNRANKED = "unranked"

    def __str__(self) -> str:
        return str(self.value)
