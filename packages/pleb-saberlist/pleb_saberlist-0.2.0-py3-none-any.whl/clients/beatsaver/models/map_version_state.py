from enum import Enum


class MapVersionState(str, Enum):
    FEEDBACK = "Feedback"
    PUBLISHED = "Published"
    SCHEDULED = "Scheduled"
    TESTPLAY = "Testplay"
    UPLOADED = "Uploaded"

    def __str__(self) -> str:
        return str(self.value)
