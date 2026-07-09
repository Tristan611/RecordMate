from spotify.auth import SpotifyAuth
from spotify.search import SpotifySearch


class SpotifyManager:

    def __init__(self, logger):

        self.logger = logger

        self.spotify = None
        self.search = None

    def start(self):

        self.logger.info("Connecting to Spotify...")

        auth = SpotifyAuth()

        self.spotify = auth.authenticate()

        self.search = SpotifySearch(self.spotify)

        self.logger.info("Spotify connected.")
