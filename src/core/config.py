from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Config:
    spotify_client_id: str = os.getenv("SPOTIFY_CLIENT_ID", "")
    spotify_client_secret: str = os.getenv("SPOTIFY_CLIENT_SECRET", "")
    spotify_redirect_uri: str = os.getenv(
        "SPOTIFY_REDIRECT_URI",
        "http://127.0.0.1:8888/callback"
    )

    acoustid_api_key: str = os.getenv("ACOUSTID_API_KEY", "")

    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    location_name: str = os.getenv("LOCATION_NAME", "Hoogeveen")
    timezone: str = os.getenv("TIMEZONE", "Europe/Amsterdam")
