from enum import Enum


class MapDifficultyCharacteristic(str, Enum):
    LAWLESS = "Lawless"
    LEGACY = "Legacy"
    LIGHTSHOW = "Lightshow"
    NOARROWS = "NoArrows"
    ONESABER = "OneSaber"
    STANDARD = "Standard"
    VALUE_3 = "90Degree"
    VALUE_4 = "360Degree"

    def __str__(self) -> str:
        return str(self.value)
