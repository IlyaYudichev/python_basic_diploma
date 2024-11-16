from typing import List, Dict, Optional, Any, Tuple
from telebot.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import bot
from states.movie_search_states import MovieSearchState
from keyboards.reply.genres_reply_markup import genres_keyboard, genres_variants
from api.api_site_request import api_request
from utils.pagination_data import get_pagination_data
from utils.result_message import send_result_message


@bot.message_handler(commands=["movie_search"])
def movie_by_name(message: Message) -> None:
    bot.set_state(message.from_user.id, MovieSearchState.name, message.chat.id)
    bot.send_message(message.from_user.id, "Введите название фильма или сериала:")


@bot.message_handler(state=MovieSearchState.name)
def get_movie_name(message: Message) -> None:
    movie_name_processed: str = message.text.strip()
    bot.set_state(message.from_user.id, MovieSearchState.genre, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["name"]: str = movie_name_processed
    bot.send_message(message.from_user.id, "Хорошо. Теперь выберите жанр:", reply_markup=genres_keyboard)


@bot.message_handler(state=MovieSearchState.genre)
def get_movie_genre(message: Message) -> None:
    if message.text.lower() in genres_variants:
        bot.set_state(message.from_user.id, MovieSearchState.number_of_results, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["genre"]: str = message.text
        bot.send_message(message.from_user.id,
                         "Отлично! Сколько результатов вывести на экран?",
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.from_user.id, "Выберите жанр из предложенных ниже:")


@bot.message_handler(state=MovieSearchState.number_of_results)
def get_number_of_results_and_send_result(message: Message) -> None:
    try:
        number_of_results: int = int(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["number_of_results"]: int = number_of_results
            url_movie_search_endswith: str = "v1.4/movie/search"
            movie_search_params: dict = {"query": data["name"],
                                         "page": 1
                                         }

            response_movie_search: dict = api_request(url_movie_search_endswith, movie_search_params)
            if response_movie_search["docs"]:
                response_filtered_by_genre: List[Dict[str, Optional[Any]]] = [i_movie for i_movie in
                                                                              response_movie_search["docs"] for
                                                                              i_genre_name in i_movie["genres"] if
                                                                              i_genre_name["name"] == data["genre"]]
                if response_filtered_by_genre:
                    response_limited: List[Dict[str, Optional[Any]]] = response_filtered_by_genre[
                                                                       :data["number_of_results"]]
                    response_movie_search["docs"]: List[Dict[str, Optional[Any]]] = response_limited
                    data["pagination_info"]: Tuple[list, list] = get_pagination_data(response_movie_search)
        if response_movie_search["docs"]:
            send_result_message(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.from_user.id,
                                 "К сожалению, по вашему запросу ничего не найдено. Попробуйте снова.")
    except ValueError:
        bot.reply_to(message,
                     "Ошибка - введенное значение должно быть целым числом.\nСколько результатов вывести на экран?")


@bot.callback_query_handler(func=lambda callback: callback.data.split('#')[0] == "movie")
def movie_page_callback(callback: CallbackQuery) -> None:
    page: int = int(callback.data.split("#")[1])
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    send_result_message(callback.from_user.id, callback.message.chat.id, page)


@bot.callback_query_handler(func=lambda callback: callback.data == "hide")
def delete_markup(callback: CallbackQuery) -> None:
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
