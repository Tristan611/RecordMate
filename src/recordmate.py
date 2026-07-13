from recognition.manager import RecognitionManager
from spotify.manager import SpotifyManager
from core.state import State
from core.state_manager import StateManager
from audio.manager import AudioManager

class RecordMate:

    def __init__(self):
        self.recognition_manager = RecognitionManager()
        self.state = StateManager()
        self.audio_manager = AudioManager()

        self.spotify_manager = SpotifyManager()
        self.spotify_manager.start()

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

        recognized_track = await self.recognition_manager.recognize(audio_file)
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

        success = self.spotify_manager.play(recognized_track)

        if not success:
            self.state.set(State.ERROR)
            print("Spotify playback mislukt.")
            return
        self.state.set(State.PLAYING)
        print("OK: Playback gestart")

        #
        # Terug naar IDLE
        #
        self.state.set(State.IDLE)