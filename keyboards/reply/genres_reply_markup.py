from logging import getLogger, WARNING
from typing import Dict, List

from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from api.api_site_request import api_request
from config_data.logger_config import configure_logger

logger = getLogger(__name__)
configure_logger(level=WARNING)

URL_GENRES_ENDSWITH: str = "v1/movie/possible-values-by-field"
GENRES_REQUEST_PARAMS: Dict[str, str] = {"field": "genres.name"}
try:
    response_genres_variants: List[Dict[str, str]] = api_request(URL_GENRES_ENDSWITH, GENRES_REQUEST_PARAMS)
    genres_variants: List[str] = [i_genre["name"] for i_genre in response_genres_variants]
    buttons_list: List[KeyboardButton] = [KeyboardButton(genre) for genre in genres_variants]
    genres_keyboard = ReplyKeyboardMarkup()
    genres_keyboard.add(*buttons_list, row_width=3)
except TypeError:
    logger.exception("Error while receiving response from API service")
    print("Неполадки на сайте https://api.kinopoisk.dev/documentation")
