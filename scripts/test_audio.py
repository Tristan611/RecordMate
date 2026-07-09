import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from core.logger import setup_logger
from audio.manager import AudioManager


def main():
    logger = setup_logger("INFO")
    audio = AudioManager(logger)

    audio.start()
    audio.record_sample(duration=10)


if __name__ == "__main__":
    main()