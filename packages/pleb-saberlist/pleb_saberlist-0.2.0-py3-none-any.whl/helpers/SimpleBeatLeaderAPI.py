from datetime import datetime, timedelta
import base64
import json
import os
import random
import requests
import time

import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

class SimpleBeatLeaderAPI:
    BASE_URL = "https://api.beatleader.xyz"

    def __init__(self, cache_expiry_days=1):
        self.session = requests.Session()
        self.cache_expiry_days = cache_expiry_days
        self.CACHE_DIR = self._determine_cache_dir()
        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)

    def _determine_cache_dir(self):
        home_cache = os.path.expanduser("~/.cache")
        saberlist_cache = os.path.join(home_cache, "saberlist")
        
        if os.path.exists(home_cache):
            if not os.path.exists(saberlist_cache):
                try:
                    os.makedirs(saberlist_cache)
                    logging.info(f"Created cache directory: {saberlist_cache}")
                except OSError as e:
                    logging.warning(f"Failed to create {saberlist_cache}: {e}")
                    return os.path.join(os.getcwd(), ".cache")
            return saberlist_cache
        else:
            logging.info("~/.cache doesn't exist, using local .cache directory")
            return os.path.join(os.getcwd(), ".cache")

    def _get_cache_filename(self, player_id):
        return os.path.join(self.CACHE_DIR, f"player_{player_id}_scores.json")

    def _is_cache_valid(self, cache_file):
        if not os.path.exists(cache_file):
            return False
        file_modified_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        return datetime.now() - file_modified_time < timedelta(days=self.cache_expiry_days)

    def get_player_scores(self, player_id, use_cache=True, page_size=100, max_pages=None):
        cache_file = self._get_cache_filename(player_id)

        if use_cache and self._is_cache_valid(cache_file):
            logging.debug(f"Using cached data for player {player_id}")
            with open(cache_file, 'r') as f:
                return json.load(f)

        logging.debug(f"Fetching fresh data for player {player_id}")
        url = f"{self.BASE_URL}/player/{player_id}/scores"
        
        all_scores = []
        page = 1
        total_items = None

        while max_pages is None or page <= max_pages:
            params = {
                "page": page,
                "count": page_size
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            all_scores.extend(data['data'])

            if total_items is None:
                total_items = data['metadata']['total']

            if len(all_scores) >= total_items:
                break

            page += 1
            time.sleep(1)  # Add a small delay to avoid rate limiting

        result = {
            'metadata': {
                'total': total_items,
                'itemsPerPage': page_size,
                'page': page
            },
            'data': all_scores
        }

        with open(cache_file, 'w') as f:
            json.dump(result, f)

        return result

    def clear_cache(self, player_id=None):
        if player_id:
            cache_file = self._get_cache_filename(player_id)
            if os.path.exists(cache_file):
                os.remove(cache_file)
                logging.debug(f"Cleared cache for player {player_id}")
        else:
            for file in os.listdir(self.CACHE_DIR):
                os.remove(os.path.join(self.CACHE_DIR, file))
            logging.debug("Cleared all cache")

    def get_cache_dir(self):
        return self.CACHE_DIR


    def get_player_info(self, player_id):
        """
        Retrieve information for a specific player.

        :param player_id: ID of the player
        :return: Dictionary containing player information
        """
        url = f"{self.BASE_URL}/player/{player_id}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            player_data = response.json()
            
            return player_data
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching player info for ID {player_id}: {e}")
            return None