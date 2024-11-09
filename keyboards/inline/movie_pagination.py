from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton


class MoviePaginator(InlineKeyboardPaginator):
    first_page_label = '<<'
    previous_page_label = '<'
    current_page_label = '· {} ·'
    next_page_label = '>'
    last_page_label = '>>'


def get_movie_paginator(movie_pages, page=1) -> MoviePaginator:
    paginator = MoviePaginator(
        len(movie_pages),
        current_page=page,
        data_pattern="movie#{page}"
    )

    button_hide = InlineKeyboardButton("Скрыть", callback_data="hide")
    paginator.add_after(button_hide)
    return paginator
