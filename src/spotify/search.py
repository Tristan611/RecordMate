class SpotifySearch:

    def __init__(self, spotify):

        self.spotify = spotify

    def search_track(self, artist, track):

        query = f"artist:{artist} track:{track}"

        result = self.spotify.search(
            q=query,
            type="track",
            limit=1
        )

        items = result["tracks"]["items"]

        if not items:
            return None

        return items[0]
