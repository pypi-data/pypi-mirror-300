import argparse
import json
import os
import sys
import logging
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List

from dotenv import load_dotenv
load_dotenv()
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
HISTORY_FILE = os.environ.get('HISTORY_FILE', "playlist_history.json")
CACHE_EXPIRY_DAYS = int(os.environ.get('CACHE_EXPIRY_DAYS', 7))

import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=LOG_LEVEL
)

from helpers.PlaylistBuilder import PlaylistBuilder
from helpers.ScoreSaberAPI import ScoreSaberAPI
from helpers.BeatLeaderAPI import BeatLeaderAPI

def load_history() -> Dict[str, Any]:
    """
    Load the playlist history from a JSON file.
    
    :return: A dictionary containing the history.
    """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_history(history: Dict[str, Any]) -> None:
    """
    Save the playlist history to a JSON file.
    
    :param history: The history dictionary to save.
    """
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def prompt_for_player_id(default_id: str = '76561199407393962') -> str:
    """
    Prompt the user to enter a ScoreSaber or BeatLeader player ID.
    Uses a default ID if the user presses Enter without input.
    
    :param default_id: The default player ID to use.
    :return: The player ID entered by the user or the default.
    """
    prompt = f"Enter player ID (press Enter for default '{default_id}'): "
    player_id = input(prompt).strip() or default_id
    return player_id

def format_time_ago(time_difference: timedelta) -> str:
    """
    Format a timedelta object into a human-readable string.
    
    :param time_difference: The time difference to format.
    :return: A string representing the time difference (e.g., '5d', '2w').
    """
    days = time_difference.days
    
    if days < 7:
        return f"{days} day(s)"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} week(s)"
    elif days < 365:
        months = days // 30
        return f"{months} month(s)"
    else:
        years = days // 365
        return f"{years} year(s)"

def normalize_difficulty_name(difficulty_name):
    difficulty_names = {
        # ScoreSaber
        '_ExpertPlus_SoloStandard': 'expertplus',
        '_Expert_SoloStandard': 'expert',
        '_Hard_SoloStandard': 'hard',
        '_Normal_SoloStandard': 'normal',
        '_Easy_SoloStandard': 'easy',
        # BeatLeader
        1: 'easy',
        3: 'normal',
        5: 'hard',
        7: 'expert',
        9: 'expertplus',
    }
    
    # Return the mapped value or the original name if there is no mapping
    return difficulty_names.get(difficulty_name, difficulty_name)

def playlist_strategy_scoresaber_oldscores(
    api: ScoreSaberAPI, 
    song_count: int = 20  # Total number of songs to select
) -> List[Dict[str, Any]]:
    """Build and format a list of songs based on old scores from ScoreSaber, avoiding reusing the same song+difficulty."""
    
    player_id = prompt_for_player_id()
    history = load_history()
    history.setdefault('scoresaber_oldscores', {})
    
    scores_data = api.get_player_scores(player_id, use_cache=True)
    all_scores = scores_data.get('playerScores', [])
    if not all_scores:
        logging.warning(f"No scores found for player ID {player_id}.")
        return []
    logging.debug(f"Found {len(all_scores)} scores for player ID {player_id}.")
    
    # Sort scores by timeSet in ascending order (oldest first)
    all_scores.sort(key=lambda x: x['score'].get('timeSet', ''))
    
    playlist_data = []
    current_time = datetime.now(timezone.utc)
    
    for score in all_scores:
        leaderboard = score.get('leaderboard', {})
        song_id = leaderboard.get('songHash')
        difficulty_raw = leaderboard.get('difficulty', {}).get('difficultyRaw', '')
        
        if not song_id or not difficulty_raw:
            logging.debug(f"Skipping score due to missing song_id or difficulty_raw: {score}")
            continue  # Skip if essential data is missing
        
        # Calculate time ago
        time_set_str = score['score'].get('timeSet')
        if not time_set_str:
            logging.debug(f"Skipping score due to missing timeSet: {score}")
            continue  # Skip if time_set is missing
        try:
            time_set = datetime.fromisoformat(time_set_str.replace('Z', '+00:00'))
        except ValueError as e:
            logging.error(f"Invalid time format for score ID {score['score'].get('id')}: {e}")
            continue
        time_difference = current_time - time_set
        time_ago = format_time_ago(time_difference)
        
        # Normalize the difficulty name
        difficulty = normalize_difficulty_name(difficulty_raw)
        game_mode = leaderboard.get('difficulty', {}).get('gameMode', 'Standard')
        if 'Standard' in game_mode:
            game_mode = 'Standard'
        
        # Check history to avoid reusing song+difficulty
        if song_id in history['scoresaber_oldscores'] and difficulty in history['scoresaber_oldscores'][song_id]:
            logging.debug(f"Skipping song {song_id} with difficulty {difficulty} as it's in history.")
            continue  # Skip if already used
        
        # Format the song data as expected by PlaylistBuilder
        song_dict = {
            'hash': song_id,
            'songName': leaderboard.get('songName', 'Unknown'),
            'difficulties': [
                {
                    'name': difficulty,
                    'characteristic': game_mode
                }
            ]
        }
        
        # Add the song to the playlist
        playlist_data.append(song_dict)
        logging.debug(f"Selected song for playlist: {song_dict['songName']} ({difficulty})")
        
        # Log the song addition
        mapper = "Unknown"  # Mapper information can be added if available
        logging.info(f"Song added: {song_dict['songName']} ({difficulty}), mapped by {mapper}. Last played {time_ago} ago.")
        
        # Check if the desired number of songs has been reached
        if len(playlist_data) >= song_count:
            logging.debug(f"Reached the desired song count: {song_count}.")
            break
    
    # Log if no songs were added
    if not playlist_data:
        logging.info("No new songs found to add to the playlist based on history.")
    else:
        logging.info(f"Total songs added to playlist: {len(playlist_data)}")
    
    # Update history to avoid reusing the same song+difficulty
    for song in playlist_data:
        song_id = song['hash']
        difficulty_name = song['difficulties'][0]['name']
        history['scoresaber_oldscores'].setdefault(song_id, []).append(difficulty_name)
    save_history(history)
    
    return playlist_data

def playlist_strategy_beatleader_oldscores(
    api: BeatLeaderAPI,
    song_count: int = 20
) -> List[Dict[str, Any]]:
    """
    Build and format a list of songs based on old scores from BeatLeader,
    avoiding reusing the same song+difficulty.

    The playlist will consist of song hashes and their corresponding difficulties.
    """
    
    player_id = prompt_for_player_id()
    history = load_history()
    history.setdefault('beatleader_oldscores', {})

    scores_data = api.get_player_scores(player_id)
    all_scores = scores_data.get('playerScores', [])
    if not all_scores:
        logging.warning(f"No scores found for player ID {player_id} on BeatLeader.")
        return []
    logging.debug(f"Found {len(all_scores)} scores for player ID {player_id} on BeatLeader.")

    # Sort scores by epochTime in ascending order (oldest first)
    all_scores.sort(key=lambda x: x.get('score', {}).get('epochTime', 0))

    playlist_data = []
    current_time = datetime.now(timezone.utc)

    for score_entry in all_scores:
        if len(playlist_data) >= song_count:
            break  # Stop if we've reached the desired number of songs

        score = score_entry.get('score', {})
        leaderboard = score_entry.get('leaderboard', {})
        
        song_hash = leaderboard.get('songHash')
        difficulty_raw = int(leaderboard.get('difficulty', ''))
        game_mode = leaderboard.get('modeName', 'Standard')
        epoch_time = score.get('epochTime')

        if not song_hash or not difficulty_raw or not epoch_time:
            logging.debug(f"Skipping score due to missing song_hash or difficulty_raw: {score_entry}")
            continue

        difficulty = normalize_difficulty_name(difficulty_raw)

        # avoid reusing song+difficulty
        if song_hash in history['beatleader_oldscores'] and difficulty in history['beatleader_oldscores'][song_hash]:
            logging.debug(f"Skipping song {song_hash} with difficulty {difficulty} as it's in history.")
            continue  # Skip if already used

        # Calculate time ago
        try:
            time_set = datetime.fromtimestamp(epoch_time, tz=timezone.utc)
        except (ValueError, OSError) as e:
            logging.error(f"Invalid epochTime for score ID {score.get('id')}: {e}")
            continue
        time_difference = current_time - time_set
        time_ago = format_time_ago(time_difference)

        # Format the song data for PlaylistBuilder
        song_dict = {
            'hash': song_hash,
            'difficulties': [
                {
                    'name': difficulty,
                    'characteristic': game_mode
                }
            ]
        }

        # Add the song to the playlist
        playlist_data.append(song_dict)
        logging.debug(f"Selected song for playlist: Hash={song_hash}, Difficulty={difficulty}. Last played {time_ago} ago.")

        # Update history
        history['beatleader_oldscores'].setdefault(song_hash, []).append(difficulty)

    # Log the final playlist
    if not playlist_data:
        logging.info("No new songs found to add to the playlist based on history for BeatLeader.")
    else:
        for song in playlist_data:
            song_hash = song['hash']
            difficulty = song['difficulties'][0]['name']
            logging.info(f"Song added: Hash={song_hash}, Difficulty={difficulty}.")
        logging.info(f"Total songs added to playlist from BeatLeader: {len(playlist_data)}")

    save_history(history)

    return playlist_data

def saberlist() -> None:
    """
    Generate a playlist of songs from a range of difficulties, all with scores previously set a long time ago.
    The range of difficulties ensures that the first few songs are good for warming up.
    Avoids reusing the same song+difficulty in a playlist based on history.
    """
    strategy = get_strategy()
    if strategy == 'scoresaber_oldscores':
        api = ScoreSaberAPI(cache_expiry_days=CACHE_EXPIRY_DAYS)
    elif strategy == 'beatleader_oldscores':
        api = BeatLeaderAPI(cache_expiry_days=CACHE_EXPIRY_DAYS)
    else:
        logging.error(f"Unknown strategy '{strategy}'")
        return

    timestamp = datetime.now().strftime("%y%m%d_%H%M")
    playlist_name = f"{strategy}-{timestamp}"

    if strategy == 'scoresaber_oldscores':
        playlist_data = playlist_strategy_scoresaber_oldscores(api)
    elif strategy == 'beatleader_oldscores':
        playlist_data = playlist_strategy_beatleader_oldscores(api)

    if not playlist_data:
        logging.info("No new scores found to add to the playlist.")
        return

    PlaylistBuilder().create_playlist(
        playlist_data,
        playlist_title=playlist_name,
        playlist_author="SaberList Tool"
    )

def get_strategy():
    parser = argparse.ArgumentParser(description="Generate Beat Saber playlists")
    parser.add_argument("-s", "--strategy", 
                        choices=["scoresaber_oldscores", "beatleader_oldscores"],
                        help="Specify the playlist generation strategy", 
                        required=True)
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    return args.strategy