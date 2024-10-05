from enum import Enum


class Operation(str, Enum):
    ALL = "all"
    ANY = "any"
    NOT = "not"

    def __str__(self) -> str:
        return str(self.value)
