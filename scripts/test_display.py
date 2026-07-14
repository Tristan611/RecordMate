import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class DisplayTest(QWidget):

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
                font-size: 32px;
            }
            """
        )

        title = QLabel("RecordMate")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        status = QLabel("Waiting for music...")
        status.setObjectName("status")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.setContentsMargins(80, 80, 80, 80)
        layout.setSpacing(30)
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(status)
        layout.addStretch()

        self.setLayout(layout)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            return

        super().keyPressEvent(event)


def main() -> None:
    app = QApplication(sys.argv)

    window = DisplayTest()
    window.showFullScreen()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()