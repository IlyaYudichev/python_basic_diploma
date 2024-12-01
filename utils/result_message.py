from telebot.apihelper import ApiTelegramException
from telegram_bot_pagination import InlineKeyboardPaginator

from loader import bot
from keyboards.inline.movie_pagination import get_movie_paginator


def send_result_message(user_id: int, chat_id: int, page: int=1):
    """
    Send message with result of movie search.

    :param user_id: user id
    :type user_id: int
    :param chat_id: chat id
    :type chat_id: int
    :param page: current page number
    :type page: int
    """
    with bot.retrieve_data(user_id, chat_id) as data:
        movie_posters, movie_pages = data["pagination_info"]
    paginator: InlineKeyboardPaginator = get_movie_paginator(movie_pages, page)
    try:
        bot.send_photo(
            user_id,
            movie_posters[page - 1],
            caption=movie_pages[page - 1],
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )
    except ApiTelegramException:
        bot.delete_state(user_id, chat_id)
        bot.send_message(chat_id, "Ой, похоже на сервере произошла ошибка.\nПожалуйста, повторите поиск.")
