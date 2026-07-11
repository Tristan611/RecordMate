import os
import sys
import asyncio
import json

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from recognition.shazam import ShazamRecognizer


async def main():
    recognizer = ShazamRecognizer()

    result = await recognizer.recognize("recordings/sample.wav")

    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())