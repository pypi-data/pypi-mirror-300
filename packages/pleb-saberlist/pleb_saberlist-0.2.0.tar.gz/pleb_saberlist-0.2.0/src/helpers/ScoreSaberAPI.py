import json
import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from clients.scoresaber import client as scoresaber_client
from clients.scoresaber.api.players import get_api_player_player_id_scores
from clients.scoresaber.models import PlayerScoreCollection

logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

class ScoreSaberAPI:
    BASE_URL = "https://scoresaber.com"

    def __init__(self, cache_expiry_days: int = 1, cache_dir: Optional[str] = None):
        self.client = scoresaber_client.Client(base_url=self.BASE_URL)
        self.cache_expiry_days = cache_expiry_days
        self.CACHE_DIR = cache_dir or self._determine_cache_dir()
        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)
            logging.info(f"Created cache directory: {self.CACHE_DIR}")

    def _determine_cache_dir(self) -> str:
        home_cache = os.path.expanduser("~/.cache")
        scoresaber_cache = os.path.join(home_cache, "scoresaber")
        
        if os.path.exists(home_cache):
            if not os.path.exists(scoresaber_cache):
                try:
                    os.makedirs(scoresaber_cache)
                    logging.info(f"Created cache directory: {scoresaber_cache}")
                except OSError as e:
                    logging.warning(f"Failed to create {scoresaber_cache}: {e}")
                    return os.path.join(os.getcwd(), ".cache")
            return scoresaber_cache
        else:
            logging.info("~/.cache doesn't exist, using local .cache directory")
            return os.path.join(os.getcwd(), ".cache")

    def _get_cache_filename(self, player_id: str) -> str:
        return os.path.join(self.CACHE_DIR, f"player_{player_id}_scores.json")

    def _is_cache_valid(self, cache_file: str) -> bool:
        if not os.path.exists(cache_file):
            return False
        file_modified_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        return datetime.now() - file_modified_time < timedelta(days=self.cache_expiry_days)

    def get_player_scores(
        self, 
        player_id: str, 
        use_cache: bool = True, 
        limit: int = 100, 
        sort: str = "recent", 
        max_pages: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches all player scores for a given player ID, handling pagination and caching.

        :param player_id: The ScoreSaber player ID.
        :param use_cache: Whether to use cached data if available.
        :param limit: Number of scores per page.
        :param sort: Sorting criteria.
        :param max_pages: Maximum number of pages to fetch. Fetch all if None.
        :return: A dictionary containing metadata and a list of player scores.
        """
        cache_file = self._get_cache_filename(player_id)

        if use_cache and self._is_cache_valid(cache_file):
            logging.debug(f"Using cached data for player {player_id}")
            with open(cache_file, 'r') as f:
                return json.load(f)

        logging.debug(f"Fetching fresh data for player {player_id}")
        
        all_scores = []
        page = 1
        total_items = None

        while max_pages is None or page <= max_pages:
            try:
                response: PlayerScoreCollection = get_api_player_player_id_scores.sync(
                    client=self.client,
                    player_id=player_id,
                    page=page,
                    limit=limit,
                    sort=sort
                )
            except Exception as e:
                logging.error(f"Error fetching page {page} for player {player_id}: {e}")
                return {"metadata": {}, "playerScores": []}

            all_scores.extend([score.dict() for score in response.player_scores])

            if total_items is None:
                total_items = response.metadata.total
                logging.debug(f"Total scores to fetch: {total_items}")

            logging.debug(f"Fetched page {page}: {len(response.player_scores)} scores")

            if len(all_scores) >= total_items:
                break

            page += 1

        result = {
            'metadata': response.metadata.dict(),
            'playerScores': all_scores
        }

        with open(cache_file, 'w') as f:
            json.dump(result, f, default=str)  # default=str to handle datetime serialization

        logging.info(f"Cached scores for player {player_id} at {cache_file}")

        return result
