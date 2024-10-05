from enum import Enum


class MapStatsSentiment(str, Enum):
    MIXED = "MIXED"
    MOSTLY_NEGATIVE = "MOSTLY_NEGATIVE"
    MOSTLY_POSITIVE = "MOSTLY_POSITIVE"
    PENDING = "PENDING"
    VERY_NEGATIVE = "VERY_NEGATIVE"
    VERY_POSITIVE = "VERY_POSITIVE"

    def __str__(self) -> str:
        return str(self.value)
