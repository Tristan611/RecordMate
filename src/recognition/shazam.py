from shazamio import Shazam

from Models.recognized_track import RecognizedTrack


class ShazamRecognizer:

    def __init__(self):
        self.shazam = Shazam()

    async def recognize(self, file_path: str):

        result = await self.shazam.recognize(file_path)

        track = result["track"]

        album = ""

        for section in track.get("sections", []):
            if section["type"] == "SONG":
                for item in section.get("metadata", []):
                    if item["title"] == "Album":
                        album = item["text"]

        return RecognizedTrack(
            title=track["title"],
            artist=track["subtitle"],
            album=album,
            cover_url=track["images"]["coverart"],
            isrc=track["isrc"],
            genre=track["genres"]["primary"]
        )