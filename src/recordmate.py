import asyncio

from audio.manager import AudioManager
from core.state import State
from core.state_manager import StateManager
from recognition.manager import RecognitionManager
from spotify.manager import SpotifyManager
from core.event_manager import EventManager
from core.events import Events

class RecordMate:
    SCAN_INTERVAL_SECONDS = 5
    AUDIO_THRESHOLD = 300.0
    LEVEL_CHECK_DURATION = 1

    def __init__(self, display):
        self.display = display

        self.events = EventManager()
        self.state = StateManager(self.events)

        self.recognition_manager = RecognitionManager()
        self.audio_manager = AudioManager()
        self.spotify_manager = SpotifyManager()

        self.current_track = None
        self.no_music_count = 0
        self.max_no_music_count = 3

        self.spotify_manager.start()

        self.events.subscribe(
            Events.TRACK_CHANGED,
            self.on_track_changed,
        )

        self.events.subscribe(
            Events.TRACK_CLEARED,
            self.on_track_cleared,
        )

        self.events.subscribe(
            Events.STATE_CHANGED,
            self.on_state_changed,
        )

    def on_state_changed(self, state: State) -> None:
        print(f"[EVENT] State gewijzigd: {state.value}")
        match state:

            case State.IDLE:
                self.display.show_idle()

            case State.LISTENING:
                self.display.show_listening()

            case State.RECOGNIZING:
                self.display.show_recognizing()

            case State.SEARCHING:
                self.display.show_searching()

            case State.PLAYING:
                # TRACK_CHANGED vult straks de titel/artiest.
                pass

            case State.ERROR:
                self.display.show_error("Something went wrong")

    def print_header(self):
        print("=" * 45)
        print("                 RecordMate")
        print("=" * 45)

    def register_no_music(self, message: str) -> None:
        self.no_music_count += 1

        print(
            f"{message} "
            f"({self.no_music_count}/{self.max_no_music_count})."
        )

        if self.no_music_count >= self.max_no_music_count:
            if self.current_track is not None:
                self.current_track = None

                self.events.emit(Events.TRACK_CLEARED)

                print("Muziek is gestopt. Huidige track is gewist.")

            self.no_music_count = 0

    def on_track_changed(self, track) -> None:

        self.display.show_playing(track)

        print(
            f"[EVENT] Nieuwe track: "
            f"{track.artist} - {track.title}"
        )

    def on_track_cleared(self) -> None:
        self.display.clear_track()

        print("[EVENT] Geen actieve track meer.")

    async def run_pipeline(self):
        #
        # IDLE / AUDIO DETECTION
        #
        self.state.set(State.IDLE)

        print("\nControleren op audiosignaal...")

        has_audio = self.audio_manager.has_audio_signal(
            threshold=self.AUDIO_THRESHOLD,
            duration=self.LEVEL_CHECK_DURATION,
        )

        if not has_audio:
            self.register_no_music("Geen muziek gedetecteerd")
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

        recognized_track = await self.recognition_manager.recognize(
            audio_file
        )

        if recognized_track is None:
            self.register_no_music("Geen nummer herkend")
            self.state.set(State.IDLE)
            return

        # Er is een geldige track herkend.
        self.no_music_count = 0

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
        self.events.emit(
            Events.TRACK_CHANGED,
            self.current_track,
        )
        self.state.set(State.PLAYING)
        await asyncio.sleep(2)
        print("OK: Playback gestart")
        print(
            f"Current track: "
            f"{self.current_track.artist} - "
            f"{self.current_track.title}"
        )

        self.state.set(State.IDLE)

    async def run(self):
        self.print_header()

        try:
            while True:
                await self.run_pipeline()
                await asyncio.sleep(self.SCAN_INTERVAL_SECONDS)

        except asyncio.CancelledError:
            pass