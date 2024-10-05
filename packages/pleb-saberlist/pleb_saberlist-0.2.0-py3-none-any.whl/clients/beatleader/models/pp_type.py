from enum import Enum


class PpType(str, Enum):
    ACC = "acc"
    GENERAL = "general"
    PASS = "pass"
    TECH = "tech"

    def __str__(self) -> str:
        return str(self.value)
