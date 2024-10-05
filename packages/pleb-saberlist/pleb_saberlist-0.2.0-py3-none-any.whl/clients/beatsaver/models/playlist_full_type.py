from enum import Enum


class PlaylistFullType(str, Enum):
    PRIVATE = "Private"
    PUBLIC = "Public"
    SEARCH = "Search"
    SYSTEM = "System"

    def __str__(self) -> str:
        return str(self.value)
