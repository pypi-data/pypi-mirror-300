from enum import Enum


class Requirements(str, Enum):
    CHROMA = "chroma"
    CINEMA = "cinema"
    IGNORE = "ignore"
    MAPPINGEXTENSIONS = "mappingExtensions"
    NONE = "none"
    NOODLES = "noodles"
    OPTIONALPROPERTIES = "optionalProperties"
    V3 = "v3"

    def __str__(self) -> str:
        return str(self.value)
