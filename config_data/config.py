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
    ("movie_search", "Поиск фильма/сериала по названию")
)
