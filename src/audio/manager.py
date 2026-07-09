class AudioManager:

    def __init__(self, logger):
        self.logger = logger

    def start(self):
        self.logger.info("Audio Manager started.")
