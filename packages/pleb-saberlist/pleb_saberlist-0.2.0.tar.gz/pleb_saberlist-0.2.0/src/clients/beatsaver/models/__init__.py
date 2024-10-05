"""Contains all the data models used in inputs/outputs"""

from .action_response import ActionResponse
from .auth_request import AuthRequest
from .get_maps_latest_sort import GetMapsLatestSort
from .get_playlists_latest_sort import GetPlaylistsLatestSort
from .get_playlists_search_page_sort_order import GetPlaylistsSearchPageSortOrder
from .get_search_text_page_leaderboard import GetSearchTextPageLeaderboard
from .get_search_text_page_sort_order import GetSearchTextPageSortOrder
from .map_detail import MapDetail
from .map_detail_declared_ai import MapDetailDeclaredAi
from .map_detail_metadata import MapDetailMetadata
from .map_detail_tags_item import MapDetailTagsItem
from .map_detail_with_order import MapDetailWithOrder
from .map_difficulty import MapDifficulty
from .map_difficulty_characteristic import MapDifficultyCharacteristic
from .map_difficulty_difficulty import MapDifficultyDifficulty
from .map_parity_summary import MapParitySummary
from .map_stats import MapStats
from .map_stats_sentiment import MapStatsSentiment
from .map_testplay import MapTestplay
from .map_version import MapVersion
from .map_version_state import MapVersionState
from .playlist_batch_request import PlaylistBatchRequest
from .playlist_full import PlaylistFull
from .playlist_full_type import PlaylistFullType
from .playlist_page import PlaylistPage
from .playlist_search_response import PlaylistSearchResponse
from .playlist_stats import PlaylistStats
from .search_response import SearchResponse
from .user_detail import UserDetail
from .user_detail_patreon import UserDetailPatreon
from .user_detail_type import UserDetailType
from .user_diff_stats import UserDiffStats
from .user_follow_data import UserFollowData
from .user_stats import UserStats
from .vote_request import VoteRequest
from .vote_summary import VoteSummary

__all__ = (
    "ActionResponse",
    "AuthRequest",
    "GetMapsLatestSort",
    "GetPlaylistsLatestSort",
    "GetPlaylistsSearchPageSortOrder",
    "GetSearchTextPageLeaderboard",
    "GetSearchTextPageSortOrder",
    "MapDetail",
    "MapDetailDeclaredAi",
    "MapDetailMetadata",
    "MapDetailTagsItem",
    "MapDetailWithOrder",
    "MapDifficulty",
    "MapDifficultyCharacteristic",
    "MapDifficultyDifficulty",
    "MapParitySummary",
    "MapStats",
    "MapStatsSentiment",
    "MapTestplay",
    "MapVersion",
    "MapVersionState",
    "PlaylistBatchRequest",
    "PlaylistFull",
    "PlaylistFullType",
    "PlaylistPage",
    "PlaylistSearchResponse",
    "PlaylistStats",
    "SearchResponse",
    "UserDetail",
    "UserDetailPatreon",
    "UserDetailType",
    "UserDiffStats",
    "UserFollowData",
    "UserStats",
    "VoteRequest",
    "VoteSummary",
)
