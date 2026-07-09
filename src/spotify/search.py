from spotify.models import SpotifyTrack


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

        item = items[0]
        album = item["album"]
        artists = item["artists"]

        return SpotifyTrack(
            name=item["name"],
            artist=artists[0]["name"],
            album=album["name"],
            uri=item["uri"],
            cover_url=album["images"][0]["url"] if album["images"] else "",
            duration_ms=item["duration_ms"]
        )