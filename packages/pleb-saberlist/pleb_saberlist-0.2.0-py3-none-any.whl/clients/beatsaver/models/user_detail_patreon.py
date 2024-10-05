from enum import Enum


class UserDetailPatreon(str, Enum):
    NONE = "None"
    SUPPORTER = "Supporter"
    SUPPORTERPLUS = "SupporterPlus"

    def __str__(self) -> str:
        return str(self.value)
