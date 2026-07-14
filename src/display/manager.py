from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DisplayManager(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("RecordMate")

        self.setStyleSheet(
            """
            QWidget {
                background-color: #111111;
                color: white;
            }

            QLabel#title {
                font-size: 64px;
                font-weight: bold;
            }

            QLabel#status {
                font-size: 30px;
            }

            QLabel#track {
                font-size: 38px;
                font-weight: bold;
            }

            QLabel#artist {
                font-size: 24px;
                color: #bbbbbb;
            }
            """
        )

        self.title = QLabel("RecordMate")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status = QLabel("Waiting for music...")
        self.status.setObjectName("status")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.track = QLabel("")
        self.track.setObjectName("track")
        self.track.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.track.setWordWrap(True)

        self.artist = QLabel("")
        self.artist.setObjectName("artist")
        self.artist.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.artist.setWordWrap(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(80, 80, 80, 80)
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addSpacing(20)
        layout.addWidget(self.status)
        layout.addSpacing(30)
        layout.addWidget(self.track)
        layout.addWidget(self.artist)
        layout.addStretch()

        self.setLayout(layout)

    def show_idle(self):
        self.status.setText("Waiting for music...")

    def show_listening(self):
        self.status.setText("Listening...")

    def show_recognizing(self):
        self.status.setText("Recognizing...")

    def show_searching(self) -> None:
        self.status.setText("Searching Spotify...")

    def show_playing(self, track):
        print("DISPLAY -> show_playing")
        self.status.setText("Now Playing")
        self.track.setText(track.title)
        self.artist.setText(track.artist)

    def show_error(self, message: str) -> None:
        self.status.setText("Something went wrong")
        self.track.setText(message)
        self.artist.setText("")

    def clear_track(self) -> None:
        self.track.setText("")
        self.artist.setText("")
        self.status.setText("Waiting for music...")