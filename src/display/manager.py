import io
import time
from datetime import datetime

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
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class VinylWidget(QWidget):
    """
    Tekent en animeert de vinylplaat in het Now Playing-scherm.
    """

    def __init__(self, size: int = 440) -> None:
        super().__init__()

        self.setFixedSize(size, size)
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True,
        )

        self.angle = 0.0
        self.accent_color = QColor("#c89562")
        self.last_frame_time = time.perf_counter()

        self.timer = QTimer(self)
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.rotate_vinyl)

    def set_accent_color(self, color: str) -> None:
        self.accent_color = QColor(color)
        self.update()

    def start(self) -> None:
        if not self.timer.isActive():
            self.last_frame_time = time.perf_counter()
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
            print(
                "[DISPLAY] Animatie-hapering: "
                f"{frame_gap_ms:.0f} ms"
            )

        self.angle = (self.angle + 0.8) % 360
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

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

        # Basis van de vinylplaat.
        outline_pen = QPen(self.accent_color)
        outline_pen.setWidth(3)

        painter.setPen(outline_pen)
        painter.setBrush(QColor("#181818"))
        painter.drawEllipse(record_rect)

        # Groeven.
        groove_pen = QPen(
            QColor(255, 255, 255, 45)
        )
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
        highlight_pen = QPen(
            QColor(255, 255, 255, 100)
        )
        highlight_pen.setWidth(10)
        highlight_pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(highlight_pen)

        highlight_margin = int(
            self.width() * 0.11
        )

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

        # Kleinere reflectie aan de andere kant.
        secondary_pen = QPen(
            QColor(255, 255, 255, 42)
        )
        secondary_pen.setWidth(6)
        secondary_pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(secondary_pen)

        painter.drawArc(
            highlight_rect,
            198 * 16,
            34 * 16,
        )

        # Middenlabel.
        label_size = int(self.width() * 0.29)
        label_x = int(
            center_x - label_size / 2
        )
        label_y = int(
            center_y - label_size / 2
        )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.accent_color)

        painter.drawEllipse(
            label_x,
            label_y,
            label_size,
            label_size,
        )

        # Binnenring van het label.
        ring_pen = QPen(
            QColor(255, 255, 255, 85)
        )
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
        marker_pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(marker_pen)

        painter.drawLine(
            int(center_x - label_size * 0.21),
            int(center_y - label_size * 0.17),
            int(center_x + label_size * 0.05),
            int(center_y - label_size * 0.17),
        )

        # Witte marker zodat de rotatie zichtbaar is.
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
    """
    Hoofdvenster van RecordMate.

    Het scherm bevat twee pagina's:

    1. Statuspagina
       Idle, listening, recognizing, searching en error.

    2. Now Playing-pagina
       Albumcover, vinylplaat, titel, artiest en status.

    RecordMate blijft dezelfde publieke methodes gebruiken:
    show_idle(), show_listening(), show_recognizing(),
    show_searching(), show_playing() en show_error().
    """

    DEFAULT_ACCENT = "#c89562"
    BACKGROUND_COLOR = "#0d0b0b"
    PANEL_COLOR = "#151212"
    SECONDARY_TEXT_COLOR = "#aaa4a0"

    DUTCH_DAYS = (
        "maandag",
        "dinsdag",
        "woensdag",
        "donderdag",
        "vrijdag",
        "zaterdag",
        "zondag",
    )

    DUTCH_MONTHS = (
        "",
        "januari",
        "februari",
        "maart",
        "april",
        "mei",
        "juni",
        "juli",
        "augustus",
        "september",
        "oktober",
        "november",
        "december",
    )

    def __init__(self) -> None:
        super().__init__()

        self.accent_color = self.DEFAULT_ACCENT
        self.pending_cover_url: str | None = None

        self.setWindowTitle("RecordMate")
        self.setObjectName("root")
        self.setMinimumSize(1000, 650)

        # Netwerkbeheer voor het asynchroon downloaden
        # van albumhoezen.
        self.network_manager = QNetworkAccessManager(
            self
        )
        self.network_manager.finished.connect(
            self.on_cover_downloaded
        )

        self.page_stack = QStackedWidget()
        self.page_stack.setObjectName("pageStack")

        self.status_page = self.build_status_page()
        self.playing_page = self.build_playing_page()

        self.page_stack.addWidget(self.status_page)
        self.page_stack.addWidget(self.playing_page)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(self.page_stack)

        self.clock_timer = QTimer(self)
        self.clock_timer.setInterval(1000)
        self.clock_timer.timeout.connect(
            self.update_clock
        )
        self.clock_timer.start()

        self.update_clock()
        self.apply_styles()

        # RecordMate start altijd op de idlepagina.
        self.page_stack.setCurrentWidget(
            self.status_page
        )

    def build_status_page(self) -> QWidget:
        """
        Bouwt het scherm voor idle en de tussenstappen
        zoals LISTENING en RECOGNIZING.
        """

        page = QWidget()
        page.setObjectName("statusPage")

        self.brand_label = QLabel("RECORDMATE")
        self.brand_label.setObjectName("brandLabel")
        self.brand_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.clock_label = QLabel("--:--")
        self.clock_label.setObjectName("clockLabel")
        self.clock_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.date_label = QLabel("")
        self.date_label.setObjectName("dateLabel")
        self.date_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # Deze labels kunnen later worden gekoppeld
        # aan een weer-API.
        self.weather_label = QLabel("--°C")
        self.weather_label.setObjectName(
            "weatherLabel"
        )
        self.weather_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.weather_description_label = QLabel(
            "WEATHER UNAVAILABLE"
        )
        self.weather_description_label.setObjectName(
            "weatherDescriptionLabel"
        )
        self.weather_description_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.state_title_label = QLabel(
            "WAITING FOR MUSIC"
        )
        self.state_title_label.setObjectName(
            "stateTitleLabel"
        )
        self.state_title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.state_title_label.setWordWrap(True)

        self.state_detail_label = QLabel(
            "Listening for vinyl..."
        )
        self.state_detail_label.setObjectName(
            "stateDetailLabel"
        )
        self.state_detail_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.state_detail_label.setWordWrap(True)

        center_panel = QFrame()
        center_panel.setObjectName("statusCenterPanel")

        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(
            70,
            45,
            70,
            45,
        )
        center_layout.setSpacing(12)

        center_layout.addWidget(
            self.clock_label
        )
        center_layout.addWidget(
            self.date_label
        )
        center_layout.addSpacing(32)
        center_layout.addWidget(
            self.weather_label
        )
        center_layout.addWidget(
            self.weather_description_label
        )

        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(
            80,
            55,
            80,
            55,
        )
        page_layout.setSpacing(20)

        page_layout.addWidget(
            self.brand_label
        )
        page_layout.addStretch(1)
        page_layout.addWidget(
            center_panel,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        page_layout.addStretch(1)
        page_layout.addWidget(
            self.state_title_label
        )
        page_layout.addWidget(
            self.state_detail_label
        )

        return page

    def build_playing_page(self) -> QWidget:
        """
        Bouwt het bestaande Now Playing-scherm opnieuw op.
        """

        page = QWidget()
        page.setObjectName("playingPage")

        self.vinyl = VinylWidget(size=440)

        self.cover = QLabel()
        self.cover.setFixedSize(420, 420)
        self.cover.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
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
        self.left_panel.setObjectName("leftPanel")
        self.left_panel.setFixedSize(720, 540)

        self.vinyl.setParent(self.left_panel)
        self.vinyl.move(250, 45)
        self.vinyl.lower()

        self.cover.setParent(self.left_panel)
        self.cover.move(35, 55)
        self.cover.raise_()

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(
            30,
            60,
            55,
            60,
        )
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

        page_layout = QHBoxLayout(page)
        page_layout.setContentsMargins(
            55,
            55,
            55,
            55,
        )
        page_layout.setSpacing(50)

        page_layout.addWidget(self.left_panel)
        page_layout.addWidget(right_panel, 1)

        return page

    def apply_cover_shadow(self) -> None:
        """
        Geeft de albumcover een donkere slagschaduw.
        """

        shadow = QGraphicsDropShadowEffect(
            self.cover
        )
        shadow.setBlurRadius(50)
        shadow.setOffset(18, 10)
        shadow.setColor(
            QColor(0, 0, 0, 235)
        )

        self.cover.setGraphicsEffect(shadow)

    def update_clock(self) -> None:
        """
        Werkt de klok en Nederlandse datum bij.
        """

        now = datetime.now()

        day_name = self.DUTCH_DAYS[
            now.weekday()
        ]
        month_name = self.DUTCH_MONTHS[
            now.month
        ]

        self.clock_label.setText(
            now.strftime("%H:%M")
        )

        self.date_label.setText(
            f"{day_name} {now.day} "
            f"{month_name} {now.year}"
        )

    def set_weather(
        self,
        temperature: str,
        description: str,
    ) -> None:
        """
        Kan later door een WeatherManager worden gebruikt.

        Voorbeeld:
            display.set_weather(
                "21°C",
                "LICHT BEWOLKT",
            )
        """

        self.weather_label.setText(
            temperature
        )
        self.weather_description_label.setText(
            description.upper()
        )

    def apply_styles(self) -> None:
        """
        Past dezelfde RecordMate-stijl toe op
        het statusscherm en het Now Playing-scherm.
        """

        self.setStyleSheet(
            f"""
            QWidget#root {{
                background-color: {self.BACKGROUND_COLOR};
                border: 8px solid {self.accent_color};
                border-radius: 24px;
                color: white;
            }}

            QStackedWidget#pageStack {{
                background-color: transparent;
                border: none;
            }}

            QWidget#statusPage,
            QWidget#playingPage {{
                background-color: transparent;
                border: none;
            }}

            QLabel#brandLabel {{
                color: {self.accent_color};
                font-size: 20px;
                font-weight: 700;
                letter-spacing: 7px;
            }}

            QFrame#statusCenterPanel {{
                min-width: 620px;
                background-color: {self.PANEL_COLOR};
                border: 2px solid {self.accent_color};
                border-radius: 28px;
            }}

            QLabel#clockLabel {{
                color: white;
                font-size: 112px;
                font-weight: 700;
            }}

            QLabel#dateLabel {{
                color: {self.accent_color};
                font-size: 25px;
                font-weight: 500;
            }}

            QLabel#weatherLabel {{
                color: white;
                font-size: 38px;
                font-weight: 600;
            }}

            QLabel#weatherDescriptionLabel {{
                color: {self.SECONDARY_TEXT_COLOR};
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 3px;
            }}

            QLabel#stateTitleLabel {{
                color: {self.accent_color};
                font-size: 22px;
                font-weight: 700;
                letter-spacing: 4px;
            }}

            QLabel#stateDetailLabel {{
                color: {self.SECONDARY_TEXT_COLOR};
                font-size: 18px;
                font-weight: 400;
            }}

            QFrame#leftPanel,
            QWidget#rightPanel {{
                background-color: transparent;
                border: none;
            }}

            QLabel#cover {{
                background-color: #222222;
                border: none;
            }}

            QLabel#title {{
                color: white;
                font-size: 54px;
                font-weight: 700;
            }}

            QLabel#artist {{
                color: {self.accent_color};
                font-size: 28px;
            }}

            QLabel#status {{
                color: {self.accent_color};
                font-size: 21px;
                font-weight: 600;
                letter-spacing: 4px;
            }}
            """
        )

    # ---------------------------------------------------------
    # Pagina wisselen
    # ---------------------------------------------------------

    def show_status_page(self) -> None:
        """
        Toont de statuspagina.
        """
        self.page_stack.setCurrentWidget(self.status_page)

    def show_playing_page(self) -> None:
        """
        Toont het Now Playing scherm.
        """
        self.page_stack.setCurrentWidget(self.playing_page)

    # ---------------------------------------------------------
    # Status schermen
    # ---------------------------------------------------------

    def show_idle(self) -> None:
        """
        RecordMate wacht op muziek.
        """

        self.show_status_page()

        self.state_title_label.setText(
            "WAITING FOR MUSIC"
        )

        self.state_detail_label.setText(
            "Listening for vinyl..."
        )

    def show_listening(self) -> None:
        """
        Audio wordt opgenomen.
        """

        self.show_status_page()

        self.state_title_label.setText(
            "LISTENING"
        )

        self.state_detail_label.setText(
            "Recording live audio..."
        )

    def show_recognizing(self) -> None:
        """
        Audio wordt herkend.
        """

        self.show_status_page()

        self.state_title_label.setText(
            "RECOGNIZING"
        )

        self.state_detail_label.setText(
            "Identifying the current track..."
        )

    def show_searching(self) -> None:
        """
        Spotify wordt geraadpleegd.
        """

        self.show_status_page()

        self.state_title_label.setText(
            "SEARCHING"
        )

        self.state_detail_label.setText(
            "Searching Spotify..."
        )

    def show_error(
        self,
        message: str,
    ) -> None:
        """
        Foutmelding tonen.
        """

        self.show_status_page()

        self.state_title_label.setText(
            "ERROR"
        )

        self.state_detail_label.setText(
            message
        )

    # ---------------------------------------------------------
    # Now Playing
    # ---------------------------------------------------------

    def show_playing(
        self,
        track,
    ) -> None:
        """
        Toon een nieuw nummer.
        """

        self.show_playing_page()

        self.title.setText(track.title)
        self.artist.setText(track.artist)

        self.status.setText(
            "● NOW PLAYING"
        )

        self.vinyl.start()

        self.load_cover(
            track.cover_url
        )

    def clear_track(self) -> None:
        """
        Wis de huidige track.
        """

        self.title.setText(
            "RecordMate"
        )

        self.artist.clear()

        self.status.setText(
            "WAITING FOR MUSIC"
        )

        self.cover.clear()

        self.vinyl.reset()

        self.accent_color = (
            self.DEFAULT_ACCENT
        )

        self.vinyl.set_accent_color(
            self.accent_color
        )

        self.apply_styles()

        self.show_idle()

    # ---------------------------------------------------------
    # Kleine helpers
    # ---------------------------------------------------------

    def set_status_text(
        self,
        title: str,
        detail: str,
    ) -> None:
        """
        Helper om de statuslabels in één keer
        aan te passen.
        """

        self.state_title_label.setText(
            title
        )

        self.state_detail_label.setText(
            detail
        )

            # ---------------------------------------------------------
    # Albumcover downloaden
    # ---------------------------------------------------------

    def load_cover(
        self,
        cover_url: str,
    ) -> None:
        """
        Start het asynchroon downloaden van
        een albumcover.
        """

        if not cover_url:
            return

        self.pending_cover_url = cover_url

        request = QNetworkRequest(
            QUrl(cover_url)
        )

        request.setRawHeader(
            b"User-Agent",
            b"RecordMate/1.0",
        )

        self.network_manager.get(request)

    def on_cover_downloaded(
        self,
        reply: QNetworkReply,
    ) -> None:
        """
        Verwerkt een gedownloade albumcover.
        """

        try:

            if (
                reply.error()
                != QNetworkReply.NetworkError.NoError
            ):
                print(
                    "Cover kon niet geladen worden:"
                    f" {reply.errorString()}"
                )
                return

            image_bytes = bytes(
                reply.readAll()
            )

            if not image_bytes:
                print(
                    "Lege coverdownload ontvangen."
                )
                return

            pixmap = QPixmap()

            if not pixmap.loadFromData(
                image_bytes
            ):
                print(
                    "Cover kon niet worden geopend."
                )
                return

            scaled = pixmap.scaled(
                self.cover.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.cover.setPixmap(scaled)

            self.accent_color = (
                self.extract_accent_color(
                    image_bytes
                )
            )

            self.vinyl.set_accent_color(
                self.accent_color
            )

            self.apply_styles()

        except (
            OSError,
            ValueError,
        ) as error:

            print(
                f"Cover verwerken mislukt: {error}"
            )

        finally:
            reply.deleteLater()

    # ---------------------------------------------------------
    # Accentkleur bepalen
    # ---------------------------------------------------------

    def extract_accent_color(
        self,
        image_bytes: bytes,
    ) -> str:
        """
        Probeert een mooie accentkleur uit
        de albumcover te halen.
        """

        try:

            image = Image.open(
                io.BytesIO(image_bytes)
            )

            image = image.convert("RGB")
            image.thumbnail((100, 100))

            colors = image.getcolors(
                maxcolors=10000
            )

            if not colors:
                return self.DEFAULT_ACCENT

            colors.sort(reverse=True)

            for _, color in colors:

                red, green, blue = color

                brightness = (
                    red + green + blue
                ) / 3

                saturation = (
                    max(color) - min(color)
                )

                if (
                    50 < brightness < 215
                    and saturation >= 18
                ):
                    return (
                        f"#{red:02x}"
                        f"{green:02x}"
                        f"{blue:02x}"
                    )

        except Exception as error:

            print(
                "Accentkleur bepalen mislukt:"
                f" {error}"
            )

        return self.DEFAULT_ACCENT

    # ---------------------------------------------------------
    # Openbare API
    # ---------------------------------------------------------

    def set_accent_color(
        self,
        color: str,
    ) -> None:
        """
        Zet handmatig een accentkleur.
        """

        self.accent_color = color
        self.vinyl.set_accent_color(color)
        self.apply_styles()

    def reset_theme(self) -> None:
        """
        Zet de standaard RecordMate-kleuren terug.
        """

        self.set_accent_color(
            self.DEFAULT_ACCENT
        )

    # ---------------------------------------------------------
    # Destructor
    # ---------------------------------------------------------

    def closeEvent(self, event) -> None:
        """
        Netjes timers stoppen bij afsluiten.
        """

        self.clock_timer.stop()
        self.vinyl.stop()

        super().closeEvent(event)

