class DisplayManager:

    def __init__(self, logger):
        self.logger = logger

    def start(self):
        self.logger.info("Display Manager started.")
