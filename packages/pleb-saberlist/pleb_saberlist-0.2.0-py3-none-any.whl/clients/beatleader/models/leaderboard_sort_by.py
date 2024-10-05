from enum import Enum


class LeaderboardSortBy(str, Enum):
    ACC = "acc"
    DATE = "date"
    MAXSTREAK = "maxStreak"
    MISTAKES = "mistakes"
    PAUSES = "pauses"
    PP = "pp"
    RANK = "rank"
    WEIGHT = "weight"
    WEIGHTEDPP = "weightedPp"

    def __str__(self) -> str:
        return str(self.value)
