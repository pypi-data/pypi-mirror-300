from enum import Enum


class MapSortBy(str, Enum):
    ACCRATING = "accRating"
    DURATION = "duration"
    NAME = "name"
    NONE = "none"
    PASSRATING = "passRating"
    PLAYCOUNT = "playCount"
    SCORETIME = "scoreTime"
    STARS = "stars"
    TECHRATING = "techRating"
    TIMESTAMP = "timestamp"
    VOTECOUNT = "voteCount"
    VOTERATIO = "voteRatio"
    VOTING = "voting"

    def __str__(self) -> str:
        return str(self.value)
