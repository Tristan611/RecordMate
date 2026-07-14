import io

import requests
from PIL import Image
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class VinylWidget(QWidget):

    def __init__(self, size: int = 440):
        super().__init__()

        self.setFixedSize(size, size)
        self.angle = 0
        self.accent_color = QColor("#c89562")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_vinyl)

    def set_accent_color(self, color: str) -> None:
        self.accent_color = QColor(color)
        self.update()

    def start(self) -> None:
        if not self.timer.isActive():
            self.timer.start(40)

    def stop(self) -> None:
        self.timer.stop()

    def rotate_vinyl(self) -> None:
        self.angle = (self.angle + 4) % 360
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center_x = self.width() / 2
        center_y = self.height() / 2

        painter.translate(center_x, center_y)
        painter.rotate(self.angle)
        painter.translate(-center_x, -center_y)

        outer_margin = 10
        record_rect = self.rect().adjusted(
            outer_margin,
            outer_margin,
            -outer_margin,
            -outer_margin,
        )

        # Buitenrand en basis van de plaat
        outline_pen = QPen(self.accent_color)
        outline_pen.setWidth(6)

        painter.setPen(outline_pen)
        painter.setBrush(QColor("#202020"))
        painter.drawEllipse(record_rect)

        # Groeven
        groove_pen = QPen(QColor("#505050"))
        groove_pen.setWidth(2)
        painter.setPen(groove_pen)

        max_margin = int(self.width() * 0.39)

        for margin in range(28, max_margin, 15):
            groove_rect = self.rect().adjusted(
                margin,
                margin,
                -margin,
                -margin,
            )
            painter.drawEllipse(groove_rect)

        # Draaiende glansboog
        highlight_pen = QPen(QColor(255, 255, 255, 90))
        highlight_pen.setWidth(10)
        highlight_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(highlight_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        highlight_margin = int(self.width() * 0.11)
        highlight_rect = self.rect().adjusted(
            highlight_margin,
            highlight_margin,
            -highlight_margin,
            -highlight_margin,
        )

        painter.drawArc(
            highlight_rect,
            25 * 16,
            55 * 16,
        )

        # Label
        label_size = int(self.width() * 0.29)
        label_x = int(center_x - label_size / 2)
        label_y = int(center_y - label_size / 2)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.accent_color)
        painter.drawEllipse(
            label_x,
            label_y,
            label_size,
            label_size,
        )

        # Asymmetrisch stipje om rotatie zichtbaar te maken
        marker_size = 12

        painter.setBrush(QColor("#f5f5f5"))
        painter.drawEllipse(
            int(center_x + label_size * 0.22),
            int(center_y - marker_size / 2),
            marker_size,
            marker_size,
        )

        # Middengat
        hole_size = 14

        painter.setBrush(QColor("#111111"))
        painter.drawEllipse(
            int(center_x - hole_size / 2),
            int(center_y - hole_size / 2),
            hole_size,
            hole_size,
        )


class DisplayManager(QWidget):

    def __init__(self):
        super().__init__()

        self.accent_color = "#c89562"

        self.setWindowTitle("RecordMate")
        self.setObjectName("root")

        self.vinyl = VinylWidget(size=440)

        self.cover = QLabel()
        self.cover.setFixedSize(420, 420)
        self.cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover.setScaledContents(True)
        self.cover.setObjectName("cover")

        self.title = QLabel("RecordMate")
        self.title.setObjectName("title")
        self.title.setWordWrap(True)

        self.artist = QLabel("")
        self.artist.setObjectName("artist")
        self.artist.setWordWrap(True)

        self.status = QLabel("WAITING FOR MUSIC")
        self.status.setObjectName("status")

        self.left_panel = QFrame()
        self.left_panel.setFixedSize(720, 540)
        self.left_panel.setStyleSheet(
            "background: transparent; border: none;"
        )

        self.vinyl.setParent(self.left_panel)
        self.vinyl.move(250, 45)
        self.vinyl.lower()

        self.cover.setParent(self.left_panel)
        self.cover.move(35, 55)
        self.cover.raise_()

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(30, 60, 55, 60)
        text_layout.setSpacing(24)
        text_layout.addStretch()
        text_layout.addWidget(self.title)
        text_layout.addWidget(self.artist)
        text_layout.addSpacing(35)
        text_layout.addWidget(self.status)
        text_layout.addStretch()

        right_panel = QWidget()
        right_panel.setLayout(text_layout)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(55, 55, 55, 55)
        main_layout.setSpacing(70)
        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(right_panel, 1)

        self.setLayout(main_layout)
        self.apply_styles()

    def apply_styles(self) -> None:
        self.setStyleSheet(
            f"""
            QWidget#root {{
                background-color: #0d0b0b;
                border: 8px solid {self.accent_color};
                border-radius: 24px;
                color: white;
            }}

            QLabel#cover {{
                background-color: #222222;
                border: none;
            }}

            QLabel#title {{
                font-size: 54px;
                font-weight: 700;
                color: white;
            }}

            QLabel#artist {{
                font-size: 28px;
                color: {self.accent_color};
            }}

            QLabel#status {{
                font-size: 21px;
                font-weight: 600;
                letter-spacing: 4px;
                color: {self.accent_color};
            }}
            """
        )

    def show_idle(self) -> None:
        if not self.cover.pixmap():
            self.status.setText("WAITING FOR MUSIC")
            self.vinyl.stop()

    def show_listening(self) -> None:
        self.status.setText("LISTENING")

    def show_recognizing(self) -> None:
        self.status.setText("RECOGNIZING")

    def show_searching(self) -> None:
        self.status.setText("SEARCHING SPOTIFY")

    def show_playing(self, track) -> None:
        self.title.setText(track.title)
        self.artist.setText(track.artist)
        self.status.setText("● NOW PLAYING")

        self.load_cover(track.cover_url)
        self.vinyl.start()

    def clear_track(self) -> None:
        self.title.setText("RecordMate")
        self.artist.setText("")
        self.status.setText("WAITING FOR MUSIC")
        self.cover.clear()
        self.vinyl.stop()

    def show_error(self, message: str) -> None:
        self.status.setText("SOMETHING WENT WRONG")
        self.title.setText(message)

    def load_cover(self, cover_url: str) -> None:
        if not cover_url:
            return

        try:
            response = requests.get(cover_url, timeout=10)
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)

            self.cover.setPixmap(
                pixmap.scaled(
                    self.cover.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

            self.accent_color = self.extract_accent_color(
                response.content
            )

            self.vinyl.set_accent_color(self.accent_color)
            self.apply_styles()

        except requests.RequestException as error:
            print(f"Cover kon niet geladen worden: {error}")

        except (OSError, ValueError) as error:
            print(f"Cover kon niet verwerkt worden: {error}")

    def extract_accent_color(self, image_bytes: bytes) -> str:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")
        image.thumbnail((100, 100))

        colors = image.getcolors(maxcolors=10000)

        if not colors:
            return "#c89562"

        colors.sort(reverse=True)

        for _, color in colors:
            red, green, blue = color
            brightness = (red + green + blue) / 3

            if 45 < brightness < 220:
                return f"#{red:02x}{green:02x}{blue:02x}"

        return "#c89562"