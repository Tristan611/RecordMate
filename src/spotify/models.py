from dataclasses import dataclass


@dataclass
class SpotifyTrack:
    name: str
    artist: str
    album: str
    uri: str
    cover_url: str
    duration_ms: int
