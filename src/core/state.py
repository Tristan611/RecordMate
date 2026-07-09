from enum import Enum


class AppState(Enum):

    STARTING = "Starting"

    IDLE = "Idle"

    LISTENING = "Listening"

    RECOGNIZING = "Recognizing"

    PLAYING = "Playing"

    ERROR = "Error"
