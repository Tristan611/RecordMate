import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from spotify.auth import SpotifyAuth
from spotify.search import SpotifySearch


def print_line():
    print("-" * 40)


def main():
    print_line()
    print("RecordMate Spotify Test")
    print_line()

    spotify = SpotifyAuth().authenticate()

    me = spotify.current_user()

    print("Spotify connection: OK")
    print(f"User     : {me.get('display_name')}")
    print(f"Country  : {me.get('country')}")
    print(f"Product  : {me.get('product')}")

    print_line()

    search = SpotifySearch(spotify)
    track = search.search_track("Alter Bridge", "Blackbird")

    if track is None:
        print("Track search: FAILED")
        return

    album = track["album"]
    artist = track["artists"][0]

    print("Track search: OK")
    print(f"Track    : {track['name']}")
    print(f"Artist   : {artist['name']}")
    print(f"Album    : {album['name']}")
    print(f"URI      : {track['uri']}")
    print(f"Cover    : {album['images'][0]['url'] if album['images'] else 'No cover'}")

    print_line()


if __name__ == "__main__":
    main()