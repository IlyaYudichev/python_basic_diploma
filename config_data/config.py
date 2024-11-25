import os
from typing import Tuple

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к. отсутствует файл .env")
else:
    load_dotenv()


BOT_TOKEN: str = os.getenv("BOT_TOKEN")
KINOPOISK_API_KEY: str = os.getenv("KINOPOISK_API_KEY")

DEFAULT_COMMANDS: Tuple[Tuple[str, str], ...] = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("hello_world", "Тестовая команда"),
    ("movie_search", "Поиск фильмов/сериалов по названию"),
    ("movie_by_rating", "Поиск фильмов/сериалов по рейтингу"),
    ("low_budget_movie", "Поиск фильмов/сериалов с низким бюджетом"),
    ("high_budget_movie", "Поиск фильмов/сериалов с высоким бюджетом")
)
