import math
import subprocess
import wave
from array import array
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
    
    def measure_level(
        self,
        duration: int = 1,
        output_path: str = "recordings/level_probe.wav",
    ) -> float:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        command = [
            "arecord",
            "-D", self.device,
            "-f", "cd",
            "-d", str(duration),
            str(path),
        ]

        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        with wave.open(str(path), "rb") as wav_file:
            sample_width = wav_file.getsampwidth()

            if sample_width != 2:
                raise ValueError(
                    f"Onverwachte samplebreedte: {sample_width} bytes"
                )

            frames = wav_file.readframes(wav_file.getnframes())

        samples = array("h")
        samples.frombytes(frames)

        if not samples:
            return 0.0

        sum_of_squares = sum(sample * sample for sample in samples)
        rms = math.sqrt(sum_of_squares / len(samples))

        return rms