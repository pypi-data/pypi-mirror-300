from enum import Enum


class Type(str, Enum):
    ALL = "all"
    NOMINATED = "nominated"
    OST = "ost"
    QUALIFIED = "qualified"
    RANKED = "ranked"
    RANKING = "ranking"
    REWEIGHTED = "reweighted"
    REWEIGHTING = "reweighting"
    STAFF = "staff"
    UNRANKED = "unranked"

    def __str__(self) -> str:
        return str(self.value)
