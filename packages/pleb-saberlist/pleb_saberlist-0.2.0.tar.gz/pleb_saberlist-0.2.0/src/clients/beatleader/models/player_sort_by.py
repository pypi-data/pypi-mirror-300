from enum import Enum


class PlayerSortBy(str, Enum):
    ACC = "acc"
    DAILYIMPROVEMENTS = "dailyImprovements"
    HMD = "hmd"
    LASTPLAY = "lastplay"
    MAXSTREAK = "maxStreak"
    NAME = "name"
    PLAYCOUNT = "playCount"
    PP = "pp"
    RANK = "rank"
    REPLAYSWATCHED = "replaysWatched"
    SCORE = "score"
    TIMING = "timing"
    TOP1COUNT = "top1Count"
    TOP1SCORE = "top1Score"
    TOPACC = "topAcc"
    TOPPP = "topPp"
    WEIGHTEDACC = "weightedAcc"
    WEIGHTEDRANK = "weightedRank"

    def __str__(self) -> str:
        return str(self.value)
