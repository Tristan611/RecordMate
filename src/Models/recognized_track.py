from dataclasses import dataclass


@dataclass
class RecognizedTrack:
    title: str
    artist: str
    album: str
    cover_url: str
    isrc: str
    genre: str
    confidence: float | None = None