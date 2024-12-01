from random import choices
from typing import List, Dict, Optional, Any, Union, Tuple
from telebot.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import bot
from states.movie_by_rating_states import MovieByRatingStates
from keyboards.reply.genres_reply_markup import genres_keyboard, genres_variants
from utils.full_response import get_full_response
from utils.pagination_data import get_pagination_data
from utils.result_message import send_result_message


@bot.message_handler(commands=["movie_by_rating"])
def movie_by_rating_search(message: Message) -> None:
    """
    Request movie rating from user.

    :param message: message from user
    :type message: Message
    """
    bot.set_state(message.from_user.id, MovieByRatingStates.rating, message.chat.id)
    bot.send_message(message.from_user.id, "Введите рейтинг фильма/сериала:", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(state=MovieByRatingStates.rating)
def get_movie_rating(message: Message) -> None:
    """
    Check and save movie rating and request genre of movie from user.

    :param message: message from user
    :type message: Message
    :raise ValueError: raise exception if user input is not a number from 0 to 10 or contains 3 numbers
    """
    user_input: str = message.text.replace(",", ".")
    try:
        if "-" in user_input and user_input.count("-") == 1:
            range_extreme_points: List[str] = user_input.split("-")
            filtered_range: List[Optional[str]] = list(
                filter(lambda x: 0 <= float(x) <= 10, range_extreme_points))
            if len(filtered_range) != 2:
                raise ValueError
            if filtered_range[0] > filtered_range[1]:
                filtered_range.reverse()
                user_input: str = "-".join(filtered_range)
        elif not 0 <= float(user_input) <= 10:
            raise ValueError
        bot.set_state(message.from_user.id, MovieByRatingStates.genre, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["movie_rating"]: List[str] = [user_input]
        bot.send_message(message.from_user.id, "Хорошо. Теперь выберите жанр:", reply_markup=genres_keyboard)
    except ValueError:
        bot.send_message(message.from_user.id,
                         'Ошибка. Введите целое или дробное число от 0 до 10 включительно или диапазон чисел.'
                         '\nНапример "6", "7.2" или "8-10"')


@bot.message_handler(state=MovieByRatingStates.genre)
def get_movie_genre(message: Message) -> None:
    """
    Save genre of movie and request number of results from user.

    :param message: message from user
    :type message: Message
    """
    if message.text.lower() in genres_variants:
        bot.set_state(message.from_user.id, MovieByRatingStates.number_of_results, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["genre"]: str = message.text
        bot.send_message(message.from_user.id,
                         "Отлично! Сколько результатов вывести на экран?",
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.from_user.id, "Выберите жанр из предложенных ниже:")


@bot.message_handler(state=MovieByRatingStates.number_of_results)
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
            url_movie_search_endswith: str = "v1.4/movie"
            fields_required: List[str] = ["name", "description", "rating", "year", "genres", "ageRating", "poster"]
            movie_search_params: Dict[str, Union[str, int, list]] = {"page": 1,
                                                                     "limit": 250,
                                                                     "rating.kp": data["movie_rating"],
                                                                     "genres.name": data["genre"],
                                                                     "selectFields": fields_required,
                                                                     "notNullFields": ["name"]
                                                                     }
            response_movie_search: Dict[str, Optional[Any]] = get_full_response(url_movie_search_endswith,
                                                                                movie_search_params)
            if len(response_movie_search["docs"]) > data["number_of_results"]:
                result_response: List[Dict[str, Optional[Any]]] = choices(response_movie_search["docs"],
                                                                          k=data["number_of_results"])
            else:
                result_response: List[Dict[str, Optional[Any]]] = response_movie_search["docs"]
            data["pagination_info"]: Tuple[list, list] = get_pagination_data(result_response)
        if result_response:
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
