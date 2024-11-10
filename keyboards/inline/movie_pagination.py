from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton


def get_movie_paginator(movie_pages, page=1) -> InlineKeyboardPaginator:
    paginator = InlineKeyboardPaginator(
        len(movie_pages),
        current_page=page,
        data_pattern="movie#{page}"
    )

    button_hide = InlineKeyboardButton("Скрыть", callback_data="hide")
    paginator.add_after(button_hide)
    return paginator
