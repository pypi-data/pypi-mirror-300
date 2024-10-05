from enum import Enum


class ScoresSortBy(str, Enum):
    ACC = "acc"
    ACCPP = "accPP"
    DATE = "date"
    LASTTRYTIME = "lastTryTime"
    MAXSTREAK = "maxStreak"
    MISTAKES = "mistakes"
    PASSPP = "passPP"
    PAUSES = "pauses"
    PLAYCOUNT = "playCount"
    PP = "pp"
    RANK = "rank"
    REPLAYSWATCHED = "replaysWatched"
    STARS = "stars"
    TECHPP = "techPP"
    TIMING = "timing"

    def __str__(self) -> str:
        return str(self.value)
