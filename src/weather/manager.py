from dataclasses import dataclass
from datetime import datetime, timedelta

import requests


@dataclass
class WeatherData:
    temperature: float
    description: str
    weather_code: int


class WeatherManager:
    LATITUDE = 52.5168
    LONGITUDE = 6.0830

    CACHE_DURATION = timedelta(minutes=15)

    def __init__(self):
        self.last_update: datetime | None = None
        self.cached_weather: WeatherData | None = None

    def get_weather(self) -> WeatherData | None:
        #
        # Gebruik cache wanneer deze nog geldig is.
        #
        if (
            self.cached_weather is not None
            and self.last_update is not None
            and datetime.now() - self.last_update < self.CACHE_DURATION
        ):
            return self.cached_weather

        try:
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": self.LATITUDE,
                    "longitude": self.LONGITUDE,
                    "current": "temperature_2m,weather_code",
                },
                timeout=5,
            )

            response.raise_for_status()

            current = response.json()["current"]

            weather = WeatherData(
                temperature=current["temperature_2m"],
                description=self._weather_description(
                    current["weather_code"]
                ),
                weather_code=current["weather_code"],
            )

            self.cached_weather = weather
            self.last_update = datetime.now()

            print("[WEATHER] Nieuw weer opgehaald.")

            return weather

        except Exception as e:
            print(f"[WEATHER] {e}")

            #
            # Bij een fout gebruiken we de laatst bekende data.
            #
            return self.cached_weather

    def _weather_description(self, code: int) -> str:
        mapping = {
            0: "Helder",
            1: "Overwegend helder",
            2: "Licht bewolkt",
            3: "Bewolkt",
            45: "Mist",
            48: "Rijpmist",
            51: "Motregen",
            53: "Motregen",
            55: "Zware motregen",
            61: "Regen",
            63: "Regen",
            65: "Zware regen",
            71: "Sneeuw",
            73: "Sneeuw",
            75: "Zware sneeuw",
            80: "Regenbuien",
            81: "Regenbuien",
            82: "Zware regenbuien",
            95: "Onweer",
        }

        return mapping.get(code, "Onbekend")