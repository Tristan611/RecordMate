import io
import time
from PIL import Image
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap
from PySide6.QtNetwork import (
    QNetworkAccessManager,
    QNetworkReply,
    QNetworkRequest,
)
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class VinylWidget(QWidget):

    def __init__(self, size: int = 440) -> None:
        super().__init__()
        self.last_frame_time = time.perf_counter()
        self.setFixedSize(size, size)
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True,
        )

        self.angle = 0.0
        self.accent_color = QColor("#c89562")

        self.timer = QTimer(self)
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.rotate_vinyl)

    def set_accent_color(self, color: str) -> None:
        self.accent_color = QColor(color)
        self.update()

    def start(self) -> None:
        if not self.timer.isActive():
            self.timer.start()

    def stop(self) -> None:
        self.timer.stop()

    def reset(self) -> None:
        self.stop()
        self.angle = 0.0
        self.update()

    def rotate_vinyl(self) -> None:
        now = time.perf_counter()
        frame_gap_ms = (now - self.last_frame_time) * 1000
        self.last_frame_time = now

        if frame_gap_ms > 120:
            print(f"[DISPLAY] Animatie-hapering: {frame_gap_ms:.0f} ms")

        self.angle = (self.angle + 0.8) % 360
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center_x = self.width() / 2
        center_y = self.height() / 2

        painter.translate(center_x, center_y)
        painter.rotate(self.angle)
        painter.translate(-center_x, -center_y)

        outer_margin = 16
        record_rect = self.rect().adjusted(
            outer_margin,
            outer_margin,
            -outer_margin,
            -outer_margin,
        )

        # Subtiele gloed rondom de plaat.
        glow_color = QColor(self.accent_color)
        glow_color.setAlpha(65)

        glow_pen = QPen(glow_color)
        glow_pen.setWidth(9)

        painter.setPen(glow_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(record_rect)

        # Basis van de vinyl.
        outline_pen = QPen(self.accent_color)
        outline_pen.setWidth(3)

        painter.setPen(outline_pen)
        painter.setBrush(QColor("#181818"))
        painter.drawEllipse(record_rect)

        # Groeven.
        groove_pen = QPen(QColor(255, 255, 255, 45))
        groove_pen.setWidth(1)

        painter.setPen(groove_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        max_margin = int(self.width() * 0.39)

        for margin in range(30, max_margin, 14):
            groove_rect = self.rect().adjusted(
                margin,
                margin,
                -margin,
                -margin,
            )
            painter.drawEllipse(groove_rect)

        # Grote asymmetrische reflectie.
        highlight_pen = QPen(QColor(255, 255, 255, 100))
        highlight_pen.setWidth(10)
        highlight_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(highlight_pen)

        highlight_margin = int(self.width() * 0.11)
        highlight_rect = self.rect().adjusted(
            highlight_margin,
            highlight_margin,
            -highlight_margin,
            -highlight_margin,
        )

        painter.drawArc(
            highlight_rect,
            22 * 16,
            48 * 16,
        )

        # Kleinere reflectie aan de tegenovergestelde kant.
        secondary_pen = QPen(QColor(255, 255, 255, 42))
        secondary_pen.setWidth(6)
        secondary_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(secondary_pen)
        painter.drawArc(
            highlight_rect,
            198 * 16,
            34 * 16,
        )

        # Middenlabel.
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

        # Binnenring van het label.
        ring_pen = QPen(QColor(255, 255, 255, 85))
        ring_pen.setWidth(2)

        painter.setPen(ring_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        ring_margin = 11
        painter.drawEllipse(
            label_x + ring_margin,
            label_y + ring_margin,
            label_size - ring_margin * 2,
            label_size - ring_margin * 2,
        )

        # Asymmetrische lijn op het label.
        marker_pen = QPen(QColor("#242424"))
        marker_pen.setWidth(5)
        marker_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(marker_pen)
        painter.drawLine(
            int(center_x - label_size * 0.21),
            int(center_y - label_size * 0.17),
            int(center_x + label_size * 0.05),
            int(center_y - label_size * 0.17),
        )

        # Witte marker waarmee rotatie ook op afstand zichtbaar is.
        marker_size = 15

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#f5f5f5"))
        painter.drawEllipse(
            int(center_x + label_size * 0.23),
            int(center_y - marker_size / 2),
            marker_size,
            marker_size,
        )

        # Middengat.
        hole_size = 14

        painter.setBrush(QColor("#101010"))
        painter.drawEllipse(
            int(center_x - hole_size / 2),
            int(center_y - hole_size / 2),
            hole_size,
            hole_size,
        )


class DisplayManager(QWidget):

    DEFAULT_ACCENT = "#c89562"

    def __init__(self) -> None:
        super().__init__()

        self.accent_color = self.DEFAULT_ACCENT

        self.setWindowTitle("RecordMate")
        self.setObjectName("root")

        # Asynchroon netwerkbeheer vanuit Qt.
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(
            self.on_cover_downloaded
        )

        self.pending_cover_url: str | None = None

        self.vinyl = VinylWidget(size=440)

        self.cover = QLabel()
        self.cover.setFixedSize(420, 420)
        self.cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover.setScaledContents(False)
        self.cover.setObjectName("cover")

        self.apply_cover_shadow()

        self.title = QLabel("RecordMate")
        self.title.setObjectName("title")
        self.title.setWordWrap(True)
        self.title.setMaximumWidth(720)

        self.artist = QLabel("")
        self.artist.setObjectName("artist")
        self.artist.setWordWrap(True)
        self.artist.setMaximumWidth(720)

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
        text_layout.setSpacing(30)
        text_layout.addStretch()
        text_layout.addWidget(self.title)
        text_layout.addWidget(self.artist)
        text_layout.addSpacing(35)
        text_layout.addWidget(self.status)
        text_layout.addStretch()

        right_panel = QWidget()
        right_panel.setObjectName("rightPanel")
        right_panel.setLayout(text_layout)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(55, 55, 55, 55)
        main_layout.setSpacing(50)
        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(right_panel, 1)

        self.setLayout(main_layout)
        self.apply_styles()

    def apply_cover_shadow(self) -> None:
        shadow = QGraphicsDropShadowEffect(self.cover)
        shadow.setBlurRadius(50)
        shadow.setOffset(18, 10)
        shadow.setColor(QColor(0, 0, 0, 235))

        self.cover.setGraphicsEffect(shadow)

    def apply_styles(self) -> None:
        self.setStyleSheet(
            f"""
            QWidget#root {{
                background-color: #0d0b0b;
                border: 8px solid {self.accent_color};
                border-radius: 24px;
                color: white;
            }}

            QWidget#rightPanel {{
                background: transparent;
                border: none;
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

        self.vinyl.start()
        self.load_cover(track.cover_url)

    def clear_track(self) -> None:
        self.title.setText("RecordMate")
        self.artist.setText("")
        self.status.setText("WAITING FOR MUSIC")

        self.cover.clear()
        self.vinyl.reset()

        self.accent_color = self.DEFAULT_ACCENT
        self.vinyl.set_accent_color(self.accent_color)
        self.apply_styles()

    def show_error(self, message: str) -> None:
        self.status.setText("SOMETHING WENT WRONG")
        self.title.setText(message)

    def load_cover(self, cover_url: str) -> None:
        if not cover_url:
            return

        self.pending_cover_url = cover_url

        request = QNetworkRequest(QUrl(cover_url))
        request.setRawHeader(
            b"User-Agent",
            b"RecordMate/1.0",
        )

        self.network_manager.get(request)

    def on_cover_downloaded(
        self,
        reply: QNetworkReply,
    ) -> None:
        try:
            if reply.error() != QNetworkReply.NetworkError.NoError:
                print(
                    "Cover kon niet geladen worden: "
                    f"{reply.errorString()}"
                )
                return

            image_bytes = bytes(reply.readAll())

            if not image_bytes:
                print("Coverdownload gaf geen afbeeldingsdata terug.")
                return

            pixmap = QPixmap()

            if not pixmap.loadFromData(image_bytes):
                print("Coverdata kon niet als afbeelding worden geladen.")
                return

            scaled_pixmap = pixmap.scaled(
                self.cover.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.cover.setPixmap(scaled_pixmap)

            self.accent_color = self.extract_accent_color(
                image_bytes
            )

            self.vinyl.set_accent_color(
                self.accent_color
            )

            self.apply_styles()

        except (OSError, ValueError) as error:
            print(f"Cover kon niet verwerkt worden: {error}")

        finally:
            reply.deleteLater()

    def extract_accent_color(
        self,
        image_bytes: bytes,
    ) -> str:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")
        image.thumbnail((100, 100))

        colors = image.getcolors(maxcolors=10000)

        if not colors:
            return self.DEFAULT_ACCENT

        colors.sort(reverse=True)

        for _, color in colors:
            red, green, blue = color
            brightness = (red + green + blue) / 3

            # Vermijd bijna zwarte, witte en erg fletse kleuren.
            saturation = max(color) - min(color)

            if (
                50 < brightness < 215
                and saturation >= 18
            ):
                return (
                    f"#{red:02x}"
                    f"{green:02x}"
                    f"{blue:02x}"
                )

        return self.DEFAULT_ACCENT