from shazamio import Shazam


class ShazamRecognizer:

    def __init__(self):
        self.shazam = Shazam()

    async def recognize(self, file_path: str):
        return await self.shazam.recognize(file_path)