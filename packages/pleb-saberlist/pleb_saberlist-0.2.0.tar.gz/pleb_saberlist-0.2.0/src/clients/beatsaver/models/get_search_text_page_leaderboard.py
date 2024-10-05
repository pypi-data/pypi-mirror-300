from enum import Enum


class GetSearchTextPageLeaderboard(str, Enum):
    ALL = "All"
    BEATLEADER = "BeatLeader"
    RANKED = "Ranked"
    SCORESABER = "ScoreSaber"

    def __str__(self) -> str:
        return str(self.value)
