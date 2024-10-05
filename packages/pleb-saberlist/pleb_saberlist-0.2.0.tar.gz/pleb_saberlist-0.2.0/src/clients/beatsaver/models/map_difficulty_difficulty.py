from enum import Enum


class MapDifficultyDifficulty(str, Enum):
    EASY = "Easy"
    EXPERT = "Expert"
    EXPERTPLUS = "ExpertPlus"
    HARD = "Hard"
    NORMAL = "Normal"

    def __str__(self) -> str:
        return str(self.value)
