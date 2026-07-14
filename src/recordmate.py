import asyncio

from audio.manager import AudioManager
from core.state import State
from core.state_manager import StateManager
from recognition.manager import RecognitionManager
from spotify.manager import SpotifyManager


class RecordMate:
    SCAN_INTERVAL_SECONDS = 5
    AUDIO_THRESHOLD = 300.0
    LEVEL_CHECK_DURATION = 1

    def __init__(self):
        self.recognition_manager = RecognitionManager()
        self.state = StateManager()
        self.audio_manager = AudioManager()
        self.current_track = None

        self.spotify_manager = SpotifyManager()
        self.spotify_manager.start()

    def print_header(self):
        print("=" * 45)
        print("                 RecordMate")
        print("=" * 45)

    async def run_pipeline(self):
        #
        # IDLE / AUDIO DETECTION
        #
        self.state.set(State.IDLE)

        print("\nControleren op audiosignaal...")

        if not self.audio_manager.has_audio_signal(
            threshold=self.AUDIO_THRESHOLD,
            duration=self.LEVEL_CHECK_DURATION,
        ):
            print("Geen muziek gedetecteerd.")
            return

        #
        # LISTENING
        #
        self.state.set(State.LISTENING)

        print("\n[1/4] Audio opnemen...")
        print("      Live-opname wordt gestart...")

        audio_file = self.audio_manager.record_sample()

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

        recognized_track = await self.recognition_manager.recognize(audio_file)

        if recognized_track is None:
            print("Geen nummer herkend.")
            self.state.set(State.IDLE)
            return

        current_isrc = (
            self.current_track.isrc
            if self.current_track is not None
            else None
        )

        print(f"Current ISRC : {recognized_track.isrc}")
        print(f"Previous ISRC: {current_isrc}")

        if (
            self.current_track is not None
            and recognized_track.isrc == self.current_track.isrc
        ):
            print(
                "Nummer is al actief. "
                "Spotify wordt niet opnieuw gestart."
            )
            self.state.set(State.IDLE)
            return

        print("OK: Nieuw nummer herkend")
        print(f"    Artiest : {recognized_track.artist}")
        print(f"    Nummer  : {recognized_track.title}")
        print(f"    Album   : {recognized_track.album}")

        #
        # SEARCHING
        #
        self.state.set(State.SEARCHING)

        print("\n[3/4] Spotify zoeken en playback starten...")

        success = self.spotify_manager.play(recognized_track)

        if not success:
            self.state.set(State.ERROR)
            print("Spotify playback mislukt.")
            return

        #
        # PLAYING
        #
        self.current_track = recognized_track
        self.state.set(State.PLAYING)

        print("OK: Playback gestart")
        print(
            f"Current track: "
            f"{self.current_track.artist} - "
            f"{self.current_track.title}"
        )

        #
        # Terug naar IDLE
        #
        self.state.set(State.IDLE)

    async def run(self):
        self.print_header()

        try:
            while True:
                await self.run_pipeline()
                await asyncio.sleep(self.SCAN_INTERVAL_SECONDS)

        except asyncio.CancelledError:
            pass