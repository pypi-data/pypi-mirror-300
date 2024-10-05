"""Contains all the data models used in inputs/outputs"""

from .badge import Badge
from .check_token_body import CheckTokenBody
from .comment import Comment
from .difficulty import Difficulty
from .get_api_player_player_id_scores_sort import GetApiPlayerPlayerIdScoresSort
from .i_get_token_response import IGetTokenResponse
from .leaderboard_info import LeaderboardInfo
from .leaderboard_info_collection import LeaderboardInfoCollection
from .leaderboard_player import LeaderboardPlayer
from .metadata import Metadata
from .nat_deny_body import NatDenyBody
from .nat_qualify_body import NatQualifyBody
from .nat_replace_body import NatReplaceBody
from .player import Player
from .player_badges_type_1 import PlayerBadgesType1
from .player_collection import PlayerCollection
from .player_score import PlayerScore
from .player_score_collection import PlayerScoreCollection
from .qat_comment_body import QatCommentBody
from .qat_vote_body import QatVoteBody
from .rank_request_information import RankRequestInformation
from .rank_request_listing import RankRequestListing
from .ranking_difficulty import RankingDifficulty
from .rt_comment_body import RtCommentBody
from .rt_create_body import RtCreateBody
from .rt_vote_body import RtVoteBody
from .score import Score
from .score_collection import ScoreCollection
from .score_saber_error import ScoreSaberError
from .score_stats import ScoreStats
from .user_data import UserData
from .vote_group import VoteGroup

__all__ = (
    "Badge",
    "CheckTokenBody",
    "Comment",
    "Difficulty",
    "GetApiPlayerPlayerIdScoresSort",
    "IGetTokenResponse",
    "LeaderboardInfo",
    "LeaderboardInfoCollection",
    "LeaderboardPlayer",
    "Metadata",
    "NatDenyBody",
    "NatQualifyBody",
    "NatReplaceBody",
    "Player",
    "PlayerBadgesType1",
    "PlayerCollection",
    "PlayerScore",
    "PlayerScoreCollection",
    "QatCommentBody",
    "QatVoteBody",
    "RankingDifficulty",
    "RankRequestInformation",
    "RankRequestListing",
    "RtCommentBody",
    "RtCreateBody",
    "RtVoteBody",
    "Score",
    "ScoreCollection",
    "ScoreSaberError",
    "ScoreStats",
    "UserData",
    "VoteGroup",
)
