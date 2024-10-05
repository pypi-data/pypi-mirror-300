from enum import Enum


class UserDetailType(str, Enum):
    DISCORD = "DISCORD"
    DUAL = "DUAL"
    SIMPLE = "SIMPLE"

    def __str__(self) -> str:
        return str(self.value)
