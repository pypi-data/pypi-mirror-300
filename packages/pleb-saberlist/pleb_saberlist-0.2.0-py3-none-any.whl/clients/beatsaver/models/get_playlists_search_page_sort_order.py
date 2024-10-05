from enum import Enum


class GetPlaylistsSearchPageSortOrder(str, Enum):
    CURATED = "Curated"
    LATEST = "Latest"
    RATING = "Rating"
    RELEVANCE = "Relevance"

    def __str__(self) -> str:
        return str(self.value)
