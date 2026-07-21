from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QTime, QDate
from PySide6.QtGui import QFont


class IdlePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        self.time_label = QLabel()
        self.date_label = QLabel()
        self.weather_label = QLabel("☀️ 21°C")
        self.status_label = QLabel("Listening for vinyl...")

        self.time_label.setAlignment(Qt.AlignCenter)
        self.date_label.setAlignment(Qt.AlignCenter)
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.status_label.setAlignment(Qt.AlignCenter)

        self.time_label.setFont(QFont("Arial", 42, QFont.Bold))
        self.date_label.setFont(QFont("Arial", 18))
        self.weather_label.setFont(QFont("Arial", 18))
        self.status_label.setFont(QFont("Arial", 14))

        layout.addStretch()

        layout.addWidget(self.time_label)
        layout.addWidget(self.date_label)
        layout.addSpacing(30)
        layout.addWidget(self.weather_label)

        layout.addStretch()

        layout.addWidget(self.status_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        self.update_clock()

    def update_clock(self):
        self.time_label.setText(QTime.currentTime().toString("HH:mm"))
        self.date_label.setText(QDate.currentDate().toString("dddd d MMMM yyyy"))