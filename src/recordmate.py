from pathlib import Path

from recognition.shazam import ShazamRecognizer
from spotify.auth import SpotifyAuth
from spotify.player import SpotifyPlayer
from spotify.search import SpotifySearch
from core.state import State
from core.state_manager import StateManager
from audio.manager import AudioManager

class RecordMate:

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent

        self.recognizer = ShazamRecognizer()
        self.state = StateManager()
        self.spotify_client = SpotifyAuth().authenticate()
        self.spotify_search = SpotifySearch(self.spotify_client)
        self.spotify_player = SpotifyPlayer(self.spotify_client)
        self.audio_manager = AudioManager()

    def print_header(self):
        print("=" * 45)
        print("                 RecordMate")
        print("=" * 45)

    async def run(self):

        self.print_header()

        #
        # LISTENING
        #
        self.state.set(State.LISTENING)
        audio_file = self.audio_manager.record_sample()
        print("\n[1/4] Audio opnemen...")
        print("      Live-opname wordt gestart...")

        if not audio_file.exists():
            self.state.set(State.ERROR)
            print(f"FOUT: Audiobestand niet gevonden: {audio_file}")
            return

        print(f"OK: Audio opgenomen: {audio_file}")

        #
        # RECOGNIZING
        #
        self.state.set(State.RECOGNIZING)

        print("\n[2/4] Nummer herkennen...")

        recognized_track = await self.recognizer.recognize(str(audio_file))

        if recognized_track is None:
            self.state.set(State.ERROR)
            print("FOUT: Geen nummer herkend.")
            return

        print("OK: Nummer herkend")
        print(f"    Artiest : {recognized_track.artist}")
        print(f"    Nummer  : {recognized_track.title}")

        #
        # SEARCHING
        #
        self.state.set(State.SEARCHING)

        print("\n[3/4] Spotify zoeken...")

        spotify_track = self.spotify_search.search_track(
            recognized_track.artist,
            recognized_track.title,
        )

        if spotify_track is None:
            self.state.set(State.ERROR)
            print("FOUT: Geen Spotify-track gevonden.")
            return

        print("OK: Spotify-track gevonden")

        #
        # PLAYING
        #
        self.state.set(State.PLAYING)

        print("\n[4/4] Playback starten...")

        devices = self.spotify_player.get_devices()

        if not devices:
            self.state.set(State.ERROR)
            print("Geen apparaten gevonden.")
            return

        selected_device = next(
            (d for d in devices if d.get("is_active")),
            devices[0],
        )

        self.spotify_player.play_track(
            spotify_track.uri,
            device_id=selected_device["id"],
        )

        print("OK: Playback gestart")

        #
        # Terug naar IDLE
        #
        self.state.set(State.IDLE)