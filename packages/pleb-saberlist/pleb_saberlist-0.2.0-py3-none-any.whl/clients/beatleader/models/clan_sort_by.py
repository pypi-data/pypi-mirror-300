from enum import Enum


class ClanSortBy(str, Enum):
    ACC = "acc"
    CAPTURES = "captures"
    COUNT = "count"
    NAME = "name"
    PP = "pp"
    RANK = "rank"

    def __str__(self) -> str:
        return str(self.value)
