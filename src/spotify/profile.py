class SpotifyProfile:

    def __init__(self, spotify):
        self.spotify = spotify

    def me(self):
        return self.spotify.current_user()