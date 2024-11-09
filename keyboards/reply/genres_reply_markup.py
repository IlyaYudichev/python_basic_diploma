from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from api.api_site_request import api_request

URL_GENRES_ENDSWITH: str = "v1/movie/possible-values-by-field"
GENRES_REQUEST_PARAMS: dict = {"field": "genres.name"}

response_genres_variants: list = api_request(URL_GENRES_ENDSWITH, GENRES_REQUEST_PARAMS)
genres_variants: list = [i_genre["name"] for i_genre in response_genres_variants]
buttons_list: list = [KeyboardButton(genre) for genre in genres_variants]
genres_keyboard = ReplyKeyboardMarkup()
genres_keyboard.add(*buttons_list, row_width=3)
