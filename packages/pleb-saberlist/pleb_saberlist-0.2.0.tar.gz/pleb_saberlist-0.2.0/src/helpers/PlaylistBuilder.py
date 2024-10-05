import os
import json
import random
import base64
from datetime import datetime
import logging
from typing import List, Optional, Dict
from dataclasses import dataclass, field, asdict

@dataclass
class Difficulty:
    name: str
    characteristic: str

@dataclass
class Song:
    hash: str
    difficulties: List[Difficulty]
    key: Optional[str] = field(default=None, repr=False)
    levelId: Optional[str] = field(default=None, repr=False)
    songName: Optional[str] = field(default=None, repr=False)

    def __post_init__(self):
        # Ensure missing fields don't appear in the final output
        self.__dict__ = {k: v for k, v in self.__dict__.items() if v is not None}

@dataclass
class CustomData:
    syncURL: Optional[str] = None
    owner: Optional[str] = None
    id: Optional[str] = None
    hash: Optional[str] = None
    shared: Optional[bool] = None

@dataclass
class Playlist:
    playlistTitle: str
    songs: List[Song]
    playlistAuthor: Optional[str] = None
    image: Optional[str] = None
    coverImage: Optional[str] = None
    description: Optional[str] = None
    allowDuplicates: Optional[bool] = None
    customData: Optional[CustomData] = None

class PlaylistBuilder:
    def __init__(self, covers_dir="./covers", history_file="./playlist_history.json", output_dir=None):
        self.covers_dir = covers_dir
        self.history_file = history_file
        self.output_dir = output_dir or os.getcwd()
        self._ensure_covers_directory()
        self.history = self._load_history()
        self._save_history()

    def _ensure_covers_directory(self):
        if not os.path.exists(self.covers_dir):
            os.makedirs(self.covers_dir)
            logging.info(f"Created directory: {self.covers_dir}")

    def _load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                history = json.load(f)
                history.setdefault('cover_history', [])
                return history
        return {"cover_history": []}

    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f)

    def _get_random_unused_cover(self):
        available_covers = [f for f in os.listdir(self.covers_dir) 
                            if f.endswith('.jpg') and f not in self.history['cover_history']]
        
        if not available_covers:
            logging.warning("No unused cover images available. Using no cover.")
            return None
        
        selected_cover = random.choice(available_covers)
        self.history['cover_history'].append(selected_cover)
        self._save_history()
        return os.path.join(self.covers_dir, selected_cover)

    def _encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def create_playlist(self, playlist_data: List[Dict], playlist_title: str = "playlist", playlist_author: str = "SaberList Tool") -> str:
        """
        Create a playlist from standardized playlist data.
        
        :param playlist_data: A list of dictionaries, each containing song information
        :param playlist_title: Title of the playlist
        :param playlist_author: Author of the playlist
        :return: Path to the created playlist file
        """
        songs = []
        for song_data in playlist_data:
            difficulties = [Difficulty(**diff) for diff in song_data.get('difficulties', [])]
            songs.append(Song(
                hash=song_data['hash'],
                difficulties=difficulties,
                key=song_data.get('key'),
                levelId=song_data.get('levelId'),
                songName=song_data.get('songName')
            ))

        cover_path = self._get_random_unused_cover()
        image = self._encode_image(cover_path) if cover_path else None

        playlist = Playlist(
            playlistTitle=playlist_title,
            playlistAuthor=playlist_author,
            songs=songs,
            image=f"data:image/png;base64,{image}" if image else None,
            coverImage=cover_path,
            description=f"Playlist created by SaberList Tool on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            allowDuplicates=False,
            customData=CustomData()
        )

        playlist_dict = asdict(playlist)
        filename = os.path.join(self.output_dir, f"{playlist_title.replace(' ', '_')}.bplist")
        with open(filename, 'w') as f:
            json.dump(playlist_dict, f, indent=2)

        logging.info(f"Playlist created: {filename}")
        return filename
