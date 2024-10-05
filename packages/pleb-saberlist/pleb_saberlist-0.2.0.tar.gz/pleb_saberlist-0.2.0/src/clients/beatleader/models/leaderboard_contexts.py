from enum import Enum


class LeaderboardContexts(str, Enum):
    GENERAL = "general"
    GOLF = "golf"
    NOMODS = "noMods"
    NONE = "none"
    NOPAUSE = "noPause"
    SCPM = "sCPM"
    SPEEDRUN = "speedrun"
    SPEEDRUNBACKUP = "speedrunBackup"

    def __str__(self) -> str:
        return str(self.value)
