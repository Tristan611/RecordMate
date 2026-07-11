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

    track = await recognizer.recognize("test.wav")

    print(f"Title : {track.title}")
    print(f"Artist: {track.artist}")
    print(f"Album : {track.album}")
    print(f"Genre : {track.genre}")
    print(f"ISRC  : {track.isrc}")
    print(f"Cover : {track.cover_url}")

if __name__ == "__main__":
    asyncio.run(main())