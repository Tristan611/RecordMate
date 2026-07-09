from spotipy.oauth2 import SpotifyOAuth
import spotipy

from core.config import Config


class SpotifyAuth:

    def __init__(self):
        self.config = Config()

    def authenticate(self):

        if not self.config.spotify_client_id:
            raise ValueError("SPOTIFY_CLIENT_ID ontbreekt in .env")

        if not self.config.spotify_client_secret:
            raise ValueError("SPOTIFY_CLIENT_SECRET ontbreekt in .env")

        auth_manager = SpotifyOAuth(
            client_id=self.config.spotify_client_id,
            client_secret=self.config.spotify_client_secret,
            redirect_uri=self.config.spotify_redirect_uri,
            scope=(
                "user-read-private "
                "user-read-email "
                "user-read-playback-state "
                "user-modify-playback-state"
            ),
            cache_path=".spotify_cache",
            open_browser=True
        )

        return spotipy.Spotify(auth_manager=auth_manager)