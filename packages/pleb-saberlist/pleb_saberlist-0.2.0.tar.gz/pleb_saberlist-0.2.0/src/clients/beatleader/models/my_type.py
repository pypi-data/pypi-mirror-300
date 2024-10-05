from enum import Enum


class MyType(str, Enum):
    MYMAPS = "myMaps"
    MYNOMINATED = "myNominated"
    NONE = "none"
    OTHERSNOMINATED = "othersNominated"
    PLAYED = "played"
    UNPLAYED = "unplayed"

    def __str__(self) -> str:
        return str(self.value)
