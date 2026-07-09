import subprocess
from pathlib import Path


class AudioRecorder:
    def __init__(self, device="plughw:3,0"):
        self.device = device

    def record(self, output_path="recordings/sample.wav", duration=10):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        command = [
            "arecord",
            "-D", self.device,
            "-f", "cd",
            "-d", str(duration),
            output_path
        ]

        subprocess.run(command, check=True)

        return output_path