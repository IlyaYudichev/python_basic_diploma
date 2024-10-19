from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from api.api_site_request import api_request

url_endswith: str = "v1/movie/possible-values-by-field"
genres_request_params: dict = {"field": "genres.name"}
response_genres_variants: list = api_request(url_endswith, genres_request_params)
genres_variants: list = [i_genre["name"] for i_genre in response_genres_variants]
buttons_list = [KeyboardButton(genre) for genre in genres_variants]
genres_keyboard = ReplyKeyboardMarkup()
genres_keyboard.add(*buttons_list, row_width=3)
