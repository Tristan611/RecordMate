import subprocess
from pathlib import Path


class AudioRecorder:

    def __init__(self, device="plughw:3,0"):
        self.device = device

    def record(
        self,
        output_path="recordings/latest.wav",
        duration=3,
    ) -> Path:

        path = Path(output_path)

        path.parent.mkdir(parents=True, exist_ok=True)

        command = [
            "arecord",
            "-D", self.device,
            "-f", "cd",
            "-d", str(duration),
            str(path),
        ]

        subprocess.run(command, check=True)

        if not path.exists():
            raise FileNotFoundError(path)

        return path