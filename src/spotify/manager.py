from spotify.auth import SpotifyAuth
from spotify.player import SpotifyPlayer
from spotify.search import SpotifySearch


class SpotifyManager:

    def __init__(self, logger=None):
        self.logger = logger
        self.spotify = None
        self.search = None
        self.player = None

    def start(self):
        if self.logger:
            self.logger.info("Connecting to Spotify...")

        auth = SpotifyAuth()

        self.spotify = auth.authenticate()
        self.search = SpotifySearch(self.spotify)
        self.player = SpotifyPlayer(self.spotify)

        if self.logger:
            self.logger.info("Spotify connected.")

    def play(self, recognized_track) -> bool:
        if self.search is None or self.player is None:
            raise RuntimeError(
                "SpotifyManager is niet gestart. Roep eerst start() aan."
            )

        spotify_track = self.search.search_track(
            recognized_track.artist,
            recognized_track.title,
        )

        if spotify_track is None:
            return False

        devices = self.player.get_devices()

        if not devices:
            return False

        selected_device = next(
            (device for device in devices if device.get("is_active")),
            devices[0],
        )

        self.player.play_track(
            spotify_track.uri,
            device_id=selected_device["id"],
        )

        return True