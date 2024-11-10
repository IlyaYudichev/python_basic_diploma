from loader import bot
from keyboards.inline.movie_pagination import get_movie_paginator


def send_result_message(user_id, chat_id, page=1):
    with bot.retrieve_data(user_id, chat_id) as data:
        movie_posters, movie_pages = data["pagination_info"]
    bot.send_photo(
        user_id,
        movie_posters[page - 1],
        caption=movie_pages[page - 1],
        reply_markup=get_movie_paginator(movie_pages, page).markup,
        parse_mode='Markdown'
    )
