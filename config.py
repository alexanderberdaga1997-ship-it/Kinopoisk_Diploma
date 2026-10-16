import os

BASE_URL: str = os.getenv(
    "KINOPOISK_API_URL",
    "https://api.poiskkino.dev/v1.4",
)

API_TOKEN: str = os.getenv("KINOPOISK_API_TOKEN", "")
UI_BASE_URL: str = os.getenv(
    "KINOPOISK_UI_URL", "https://www.kinopoisk.ru"
)