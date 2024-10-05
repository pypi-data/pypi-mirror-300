from enum import Enum


class MapDetailDeclaredAi(str, Enum):
    ADMIN = "Admin"
    NONE = "None"
    SAGESCORE = "SageScore"
    UPLOADER = "Uploader"

    def __str__(self) -> str:
        return str(self.value)
