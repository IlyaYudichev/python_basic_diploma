from typing import List, Dict, Optional, Any, Tuple, Union
from telebot.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import bot
from states.movie_search_states import MovieSearchStates
from keyboards.reply.genres_reply_markup import genres_keyboard, genres_variants
from utils.full_response import get_full_response
from utils.pagination_data import get_pagination_data
from utils.result_message import send_result_message


@bot.message_handler(commands=["movie_search"])
def movie_by_name(message: Message) -> None:
    """
    Request name of movie from user.

    :param message: message from user
    :type message: Message
    """
    bot.set_state(message.from_user.id, MovieSearchStates.name, message.chat.id)
    bot.send_message(message.from_user.id, "Введите название фильма или сериала:", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(state=MovieSearchStates.name)
def get_movie_name(message: Message) -> None:
    """
    Save name of movie and request genre of movie from user.

    :param message: message from user
    :type message: Message
    """
    movie_name_processed: str = message.text.strip()
    bot.set_state(message.from_user.id, MovieSearchStates.genre, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["name"]: str = movie_name_processed
    bot.send_message(message.from_user.id, "Хорошо. Теперь выберите жанр:", reply_markup=genres_keyboard)


@bot.message_handler(state=MovieSearchStates.genre)
def get_movie_genre(message: Message) -> None:
    """
    Save genre of movie and request number of results from user.

    :param message: message from user
    :type message: Message
    """
    if message.text.lower() in genres_variants:
        bot.set_state(message.from_user.id, MovieSearchStates.number_of_results, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["genre"]: str = message.text
        bot.send_message(message.from_user.id,
                         "Отлично! Сколько результатов вывести на экран?",
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.from_user.id, "Выберите жанр из предложенных ниже:")


@bot.message_handler(state=MovieSearchStates.number_of_results)
def get_number_of_results_and_send_result(message: Message) -> None:
    """
    Save number of results and send message with result of movie search.

    :param message: message from user
    :type message: Message
    """
    try:
        number_of_results: int = abs(int(message.text))
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            bot.send_message(message.chat.id, "Выполняется поиск, ожидайте...")
            data["number_of_results"]: int = number_of_results
            url_movie_search_endswith: str = "v1.4/movie/search"
            movie_search_params: Dict[str, Union[str, int, list]] = {"query": data["name"],
                                                                     "page": 1,
                                                                     "limit": 250
                                                                     }

            response_movie_search: Dict[str, Optional[Any]] = get_full_response(url_movie_search_endswith,
                                                                          movie_search_params)
            if response_movie_search["docs"]:
                response_filtered_by_genre: List[Dict[str, Optional[Any]]] = [i_movie for i_movie in
                                                                              response_movie_search["docs"] for
                                                                              i_genre_name in i_movie["genres"] if
                                                                              i_genre_name["name"] == data["genre"]]
                if response_filtered_by_genre:
                    response_movie_search["docs"]: List[Dict[str, Optional[Any]]] = response_filtered_by_genre[:data["number_of_results"]]
                data["pagination_info"]: Tuple[list, list] = get_pagination_data(response_movie_search["docs"])
        if response_movie_search["docs"]:
            send_result_message(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.from_user.id,
                             "К сожалению, по вашему запросу ничего не найдено. Попробуйте снова.")
            bot.delete_state(message.from_user.id, message.chat.id)
    except ValueError:
        bot.reply_to(message,
                     "Ошибка - введенное значение должно быть целым числом.\nСколько результатов вывести на экран?")


@bot.callback_query_handler(func=lambda callback: callback.data.split('#')[0] == "movie")
def movie_page_callback(callback: CallbackQuery) -> None:
    """
    Show new movie page in paginator.

    :param callback: paginator callback
    :type callback: CallbackQuery
    """
    page: int = int(callback.data.split("#")[1])
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    send_result_message(callback.from_user.id, callback.message.chat.id, page)


@bot.callback_query_handler(func=lambda callback: callback.data == "hide")
def delete_markup(callback: CallbackQuery) -> None:
    """
    Delete message with result of search.

    :param callback: paginator markup
    :type callback: CallbackQuery
    """
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
