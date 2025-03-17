from typing import List
from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton


def get_movie_paginator(movie_pages: List[str], history_paginator: bool, page: int = 1) -> InlineKeyboardPaginator:
    """
    Get movie paginator object.

    :param movie_pages: list with data for movie pages
    :type movie_pages: List[str]
    :param history_paginator: flag for pagination of 'history' type
    :type history_paginator: bool
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
    if history_paginator:
        film_id: str = movie_pages[page - 1].split("#")[0]
        button_seen = InlineKeyboardButton("Просмотрен", callback_data=f"seen_{film_id}_{page}")
        button_unseen = InlineKeyboardButton("Не просмотрен", callback_data=f"unseen_{film_id}_{page}")
        paginator.add_after(button_unseen, button_seen)
    button_hide = InlineKeyboardButton("Завершить поиск", callback_data="hide")
    paginator.add_after(button_hide)
    return paginator
