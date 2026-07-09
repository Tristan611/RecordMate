from core.config import Config
from core.logger import setup_logger
from core.state import AppState

from audio.manager import AudioManager
from recognition.manager import RecognitionManager
from spotify.manager import SpotifyManager
from display.manager import DisplayManager


class RecordMate:

    def __init__(self):

        self.config = Config()
        self.logger = setup_logger(self.config.log_level)

        self.state = AppState.STARTING

        self.audio = AudioManager(self.logger)
        self.recognition = RecognitionManager(self.logger)
        self.spotify = SpotifyManager(self.logger)
        self.display = DisplayManager(self.logger)

    def startup(self):

        self.logger.info("Starting RecordMate...")

        self.audio.start()
        self.spotify.start()
        self.display.start()
        self.recognition.start()

        self.state = AppState.IDLE

        self.logger.info("RecordMate is ready.")

    def run(self):

        self.startup()

        self.logger.info(f"State: {self.state.value}")
