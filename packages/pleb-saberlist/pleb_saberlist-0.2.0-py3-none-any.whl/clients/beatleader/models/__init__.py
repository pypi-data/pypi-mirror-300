"""Contains all the data models used in inputs/outputs"""

from .achievement import Achievement
from .achievement_description import AchievementDescription
from .achievement_level import AchievementLevel
from .badge import Badge
from .ban import Ban
from .beasties_nomination import BeastiesNomination
from .besties_nomination_response import BestiesNominationResponse
from .clan import Clan
from .clan_bigger_response import ClanBiggerResponse
from .clan_global_map import ClanGlobalMap
from .clan_global_map_point import ClanGlobalMapPoint
from .clan_map_connection import ClanMapConnection
from .clan_maps_sort_by import ClanMapsSortBy
from .clan_point import ClanPoint
from .clan_ranking_response import ClanRankingResponse
from .clan_ranking_response_clan_response_full_response_with_metadata_and_container import (
    ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer,
)
from .clan_response import ClanResponse
from .clan_response_full import ClanResponseFull
from .clan_response_full_response_with_metadata import ClanResponseFullResponseWithMetadata
from .clan_sort_by import ClanSortBy
from .compact_leaderboard import CompactLeaderboard
from .compact_leaderboard_response import CompactLeaderboardResponse
from .compact_score import CompactScore
from .compact_score_response import CompactScoreResponse
from .compact_score_response_response_with_metadata import CompactScoreResponseResponseWithMetadata
from .compact_song_response import CompactSongResponse
from .controller_enum import ControllerEnum
from .criteria_commentary import CriteriaCommentary
from .difficulty_description import DifficultyDescription
from .difficulty_response import DifficultyResponse
from .difficulty_status import DifficultyStatus
from .event_player import EventPlayer
from .event_ranking import EventRanking
from .external_status import ExternalStatus
from .featured_playlist import FeaturedPlaylist
from .featured_playlist_response import FeaturedPlaylistResponse
from .follower_type import FollowerType
from .global_map_history import GlobalMapHistory
from .history_compact_response import HistoryCompactResponse
from .hmd import HMD
from .info_to_highlight import InfoToHighlight
from .leaderboard import Leaderboard
from .leaderboard_change import LeaderboardChange
from .leaderboard_clan_ranking_response import LeaderboardClanRankingResponse
from .leaderboard_contexts import LeaderboardContexts
from .leaderboard_group_entry import LeaderboardGroupEntry
from .leaderboard_info_response import LeaderboardInfoResponse
from .leaderboard_info_response_response_with_metadata import LeaderboardInfoResponseResponseWithMetadata
from .leaderboard_response import LeaderboardResponse
from .leaderboard_sort_by import LeaderboardSortBy
from .legacy_modifiers import LegacyModifiers
from .link_response import LinkResponse
from .map_diff_response import MapDiffResponse
from .map_info_response import MapInfoResponse
from .map_info_response_response_with_metadata import MapInfoResponseResponseWithMetadata
from .map_quality import MapQuality
from .map_sort_by import MapSortBy
from .mapper import Mapper
from .mapper_response import MapperResponse
from .maps_type import MapsType
from .metadata import Metadata
from .modifiers_map import ModifiersMap
from .modifiers_rating import ModifiersRating
from .my_type import MyType
from .operation import Operation
from .order import Order
from .participating_event_response import ParticipatingEventResponse
from .patreon_features import PatreonFeatures
from .player import Player
from .player_change import PlayerChange
from .player_context_extension import PlayerContextExtension
from .player_follower import PlayerFollower
from .player_followers_info_response import PlayerFollowersInfoResponse
from .player_response import PlayerResponse
from .player_response_clan_response_full_response_with_metadata_and_container import (
    PlayerResponseClanResponseFullResponseWithMetadataAndContainer,
)
from .player_response_full import PlayerResponseFull
from .player_response_with_stats import PlayerResponseWithStats
from .player_response_with_stats_response_with_metadata import PlayerResponseWithStatsResponseWithMetadata
from .player_score_stats import PlayerScoreStats
from .player_score_stats_history import PlayerScoreStatsHistory
from .player_search import PlayerSearch
from .player_social import PlayerSocial
from .player_sort_by import PlayerSortBy
from .pp_type import PpType
from .profile_settings import ProfileSettings
from .qualification_change import QualificationChange
from .qualification_commentary import QualificationCommentary
from .qualification_vote import QualificationVote
from .rank_qualification import RankQualification
from .rank_update import RankUpdate
from .rank_update_change import RankUpdateChange
from .rank_voting import RankVoting
from .ranked_map import RankedMap
from .ranked_mapper_response import RankedMapperResponse
from .replay_offsets import ReplayOffsets
from .requirements import Requirements
from .score_filter_status import ScoreFilterStatus
from .score_graph_entry import ScoreGraphEntry
from .score_improvement import ScoreImprovement
from .score_metadata import ScoreMetadata
from .score_response import ScoreResponse
from .score_response_with_acc import ScoreResponseWithAcc
from .score_response_with_my_score import ScoreResponseWithMyScore
from .score_response_with_my_score_response_with_metadata import ScoreResponseWithMyScoreResponseWithMetadata
from .scores_sort_by import ScoresSortBy
from .song import Song
from .song_response import SongResponse
from .song_status import SongStatus
from .type import Type
from .voter_feedback import VoterFeedback

__all__ = (
    "Achievement",
    "AchievementDescription",
    "AchievementLevel",
    "Badge",
    "Ban",
    "BeastiesNomination",
    "BestiesNominationResponse",
    "Clan",
    "ClanBiggerResponse",
    "ClanGlobalMap",
    "ClanGlobalMapPoint",
    "ClanMapConnection",
    "ClanMapsSortBy",
    "ClanPoint",
    "ClanRankingResponse",
    "ClanRankingResponseClanResponseFullResponseWithMetadataAndContainer",
    "ClanResponse",
    "ClanResponseFull",
    "ClanResponseFullResponseWithMetadata",
    "ClanSortBy",
    "CompactLeaderboard",
    "CompactLeaderboardResponse",
    "CompactScore",
    "CompactScoreResponse",
    "CompactScoreResponseResponseWithMetadata",
    "CompactSongResponse",
    "ControllerEnum",
    "CriteriaCommentary",
    "DifficultyDescription",
    "DifficultyResponse",
    "DifficultyStatus",
    "EventPlayer",
    "EventRanking",
    "ExternalStatus",
    "FeaturedPlaylist",
    "FeaturedPlaylistResponse",
    "FollowerType",
    "GlobalMapHistory",
    "HistoryCompactResponse",
    "HMD",
    "InfoToHighlight",
    "Leaderboard",
    "LeaderboardChange",
    "LeaderboardClanRankingResponse",
    "LeaderboardContexts",
    "LeaderboardGroupEntry",
    "LeaderboardInfoResponse",
    "LeaderboardInfoResponseResponseWithMetadata",
    "LeaderboardResponse",
    "LeaderboardSortBy",
    "LegacyModifiers",
    "LinkResponse",
    "MapDiffResponse",
    "MapInfoResponse",
    "MapInfoResponseResponseWithMetadata",
    "Mapper",
    "MapperResponse",
    "MapQuality",
    "MapSortBy",
    "MapsType",
    "Metadata",
    "ModifiersMap",
    "ModifiersRating",
    "MyType",
    "Operation",
    "Order",
    "ParticipatingEventResponse",
    "PatreonFeatures",
    "Player",
    "PlayerChange",
    "PlayerContextExtension",
    "PlayerFollower",
    "PlayerFollowersInfoResponse",
    "PlayerResponse",
    "PlayerResponseClanResponseFullResponseWithMetadataAndContainer",
    "PlayerResponseFull",
    "PlayerResponseWithStats",
    "PlayerResponseWithStatsResponseWithMetadata",
    "PlayerScoreStats",
    "PlayerScoreStatsHistory",
    "PlayerSearch",
    "PlayerSocial",
    "PlayerSortBy",
    "PpType",
    "ProfileSettings",
    "QualificationChange",
    "QualificationCommentary",
    "QualificationVote",
    "RankedMap",
    "RankedMapperResponse",
    "RankQualification",
    "RankUpdate",
    "RankUpdateChange",
    "RankVoting",
    "ReplayOffsets",
    "Requirements",
    "ScoreFilterStatus",
    "ScoreGraphEntry",
    "ScoreImprovement",
    "ScoreMetadata",
    "ScoreResponse",
    "ScoreResponseWithAcc",
    "ScoreResponseWithMyScore",
    "ScoreResponseWithMyScoreResponseWithMetadata",
    "ScoresSortBy",
    "Song",
    "SongResponse",
    "SongStatus",
    "Type",
    "VoterFeedback",
)
