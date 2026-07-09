import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from spotify.auth import SpotifyAuth
from spotify.search import SpotifySearch
from spotify.player import SpotifyPlayer


def main():
    spotify = SpotifyAuth().authenticate()

    search = SpotifySearch(spotify)
    player = SpotifyPlayer(spotify)

    track = search.search_track("Alter Bridge", "Blackbird")

    if track is None:
        print("Track not found")
        return

    devices = player.get_devices()

    print("Available devices:")
    for device in devices:
        print(f"- {device['name']} | {device['type']} | active={device['is_active']} | id={device['id']}")

    if not devices:
        print("No Spotify devices found. Open Spotify on your phone/PC or install Raspotify later.")
        return

    device_id = devices[0]["id"]

    print(f"Starting playback: {track.artist} - {track.name}")
    player.play_track(track.uri, device_id=device_id)

    print("Playback started.")


if __name__ == "__main__":
    main()