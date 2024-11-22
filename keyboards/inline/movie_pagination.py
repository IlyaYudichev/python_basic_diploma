from typing import List

from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton


def get_movie_paginator(movie_pages: List[str], page: int = 1) -> InlineKeyboardPaginator:
    """
    Get movie paginator object.

    :param movie_pages: list with data for movie pages
    :type movie_pages: List[str]
    :param page: current page number
    :type page: int
    :return: paginator object of movie pages
    :rtype: InlineKeyboardPaginator
    """
    paginator = InlineKeyboardPaginator(
        len(movie_pages),
        current_page=page,
        data_pattern="movie#{page}"
    )

    button_hide = InlineKeyboardButton("Скрыть", callback_data="hide")
    paginator.add_after(button_hide)
    return paginator
