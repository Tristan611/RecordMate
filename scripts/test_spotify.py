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
    search = SpotifySearch(spotify)

    track = search.search_track("Alter Bridge", "Blackbird")

    if track is None:
        print("Track search: FAILED")
        return

    print("Track search: OK")
    print(f"Track    : {track.name}")
    print(f"Artist   : {track.artist}")
    print(f"Album    : {track.album}")
    print(f"URI      : {track.uri}")
    print(f"Cover    : {track.cover_url}")
    print(f"Duration : {track.duration_ms} ms")
    print_line()


if __name__ == "__main__":
    main()