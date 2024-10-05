from enum import Enum


class ClanMapsSortBy(str, Enum):
    ACC = "acc"
    DATE = "date"
    PP = "pp"
    RANK = "rank"
    TOCONQUER = "toconquer"
    TOHOLD = "tohold"

    def __str__(self) -> str:
        return str(self.value)
