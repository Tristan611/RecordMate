from audio.recorder import AudioRecorder


class AudioManager:

    def __init__(self, logger=None):
        self.logger = logger
        self.recorder = AudioRecorder()

    def start(self):
        self.logger.info("Audio Manager started.")

    def record_sample(self, duration=3):

        if self.logger:
            self.logger.info(f"Recording {duration} seconds of audio...")

        path = self.recorder.record(duration=duration)

        if self.logger:
            self.logger.info(f"Audio saved to {path}")

        return path
    
    def measure_level(self, duration: int = 1) -> float:
        level = self.recorder.measure_level(duration=duration)

        if self.logger:
            self.logger.info(f"Gemeten audioniveau: {level:.2f}")

        return level
    def has_audio_signal(
        self,
        threshold: float = 100.0,
        duration: int = 1,
    ) -> bool:
        level = self.measure_level(duration=duration)

        print(f"Gemeten audioniveau: {level:.2f}")

        return level >= threshold