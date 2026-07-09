class SpotifyPlayer:

    def __init__(self, spotify):
        self.spotify = spotify

    def get_devices(self):
        return self.spotify.devices()["devices"]

    def play_track(self, track_uri, device_id=None):
        self.spotify.start_playback(
            device_id=device_id,
            uris=[track_uri]
        )