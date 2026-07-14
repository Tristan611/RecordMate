import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from audio.manager import AudioManager


def main() -> None:
    audio_manager = AudioManager()

    print("Een seconde audio meten...")

    level = audio_manager.measure_level(duration=1)

    print(f"RMS-niveau: {level:.2f}")


if __name__ == "__main__":
    main()