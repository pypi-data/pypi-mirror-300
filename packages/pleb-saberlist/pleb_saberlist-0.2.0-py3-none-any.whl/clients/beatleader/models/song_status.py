from enum import Enum


class SongStatus(str, Enum):
    BEASTSABERAWARDED = "beastSaberAwarded"
    CURATED = "curated"
    FEATUREDONCC = "featuredOnCC"
    MAPOFTHEWEEK = "mapOfTheWeek"
    NONE = "none"
    NOODLEMONDAY = "noodleMonday"

    def __str__(self) -> str:
        return str(self.value)
