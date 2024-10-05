from enum import Enum


class GetMapsLatestSort(str, Enum):
    CREATED = "CREATED"
    CURATED = "CURATED"
    FIRST_PUBLISHED = "FIRST_PUBLISHED"
    LAST_PUBLISHED = "LAST_PUBLISHED"
    UPDATED = "UPDATED"

    def __str__(self) -> str:
        return str(self.value)
