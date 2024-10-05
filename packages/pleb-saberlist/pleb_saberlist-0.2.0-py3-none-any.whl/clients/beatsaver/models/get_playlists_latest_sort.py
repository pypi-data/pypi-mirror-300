from enum import Enum


class GetPlaylistsLatestSort(str, Enum):
    CREATED = "CREATED"
    CURATED = "CURATED"
    SONGS_UPDATED = "SONGS_UPDATED"
    UPDATED = "UPDATED"

    def __str__(self) -> str:
        return str(self.value)
