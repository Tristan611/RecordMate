from recognition.shazam import ShazamRecognizer


class RecognitionManager:

    def __init__(self):
        self.recognizer = ShazamRecognizer()

    async def recognize(self, audio_file):

        return await self.recognizer.recognize(str(audio_file))