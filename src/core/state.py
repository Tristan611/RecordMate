from enum import Enum


class State(Enum):
    IDLE = "Idle"
    LISTENING = "Listening"
    RECOGNIZING = "Recognizing"
    SEARCHING = "Searching Spotify"
    PLAYING = "Playing"
    ERROR = "Error"