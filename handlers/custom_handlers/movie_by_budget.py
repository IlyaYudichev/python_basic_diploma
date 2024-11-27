from typing import List, Dict, Optional, Any, Union, Tuple
from telebot.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import bot
from states.movie_by_budget_states import MovieByBudgetStates
from keyboards.reply.budget_currency_markup import get_budget_currency_markup
from keyboards.reply.genres_reply_markup import genres_keyboard, genres_variants
from api.api_site_request import api_request
from utils.pagination_data import get_pagination_data
from utils.result_message import send_result_message


@bot.message_handler(commands=["low_budget_movie", "high_budget_movie"])
def movie_by_budget_search(message: Message) -> None:
    """
    Save kind of budget and request budget currency from user.

    :param message: message from user
    :type message: Message
    """
    bot.set_state(message.from_user.id, MovieByBudgetStates.budget_currency, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.startswith("/low"):
            data["kind_of_budget"]: str = "максимально"
        else:
            data["kind_of_budget"]: str = "минимально"
    bot.send_message(message.from_user.id, "Выберите валюту бюджета фильма/сериала:",
                     reply_markup=get_budget_currency_markup())


@bot.message_handler(state=MovieByBudgetStates.budget_currency)
def get_budget_currency(message: Message) -> None:
    """
    Save budget currency and request budget value from user.

    :param message: message from user
    :type message: Message
    """
    currency_user: str = message.text[0]
    currencies_available: Tuple[str, ...] = ("₽", "$", "€")
    if currency_user in currencies_available:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["budget_currency"]: str = currency_user
            bot.send_message(message.chat.id,
                             f"Хорошо. Теперь введите {data['kind_of_budget']} возможный бюджет для поиска",
                             reply_markup=ReplyKeyboardRemove())
            bot.set_state(message.from_user.id, MovieByBudgetStates.budget_value, message.chat.id)
    else:
        bot.send_message(message.chat.id, "Ошибка. Выберите валюту бюджета из предложенных ниже:")


@bot.message_handler(state=MovieByBudgetStates.budget_value)
def get_budget_value(message: Message) -> None:
    """
    Save budget value and request movie genre from user.

    :param message: message from user
    :type message: Message
    """
    if message.text.isdecimal():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["budget_value"]: str = message.text
        bot.set_state(message.from_user.id, MovieByBudgetStates.genre, message.chat.id)
        bot.send_message(message.chat.id, "Замечательно. Теперь давайте выберем жанр:", reply_markup=genres_keyboard)
    else:
        bot.send_message(message.chat.id, 'Ошибка. Введите целое положительное число, например "100000" или "2000000".')


@bot.message_handler(state=MovieByBudgetStates.genre)
def get_movie_genre(message: Message) -> None:
    """
    Save genre of movie and request number of results from user.

    :param message: message from user
    :type message: Message
    """
    if message.text.lower() in genres_variants:
        bot.set_state(message.from_user.id, MovieByBudgetStates.number_of_results, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["genre"]: str = message.text
        bot.send_message(message.from_user.id,
                         "Отлично! Сколько результатов вывести на экран?",
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.from_user.id, "Выберите жанр из предложенных ниже:")


@bot.message_handler(state=MovieByBudgetStates.number_of_results)
def get_number_of_results_and_send_result(message: Message) -> None:
    """
    Save number of results and send message with result of movie search.

    :param message: message from user
    :type message: Message
    """
    try:
        number_of_results: int = abs(int(message.text))
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if data["kind_of_budget"] == "максимально":
                budget_range: List[str] = [f"0-{data['budget_value']}"]
            else:
                budget_range: List[str] = [f"{data['budget_value']}-1000000000"]
            data["number_of_results"]: int = number_of_results
            url_movie_search_endswith: str = "v1.4/movie"
            fields_required: List[str] = ["name", "description", "rating", "year", "genres", "ageRating", "poster",
                                          "budget"]
            movie_search_params: Dict[str, Union[str, int, list]] = {"page": 1,
                                                                     "limit": data["number_of_results"],
                                                                     "budget.value": budget_range,
                                                                     "genres.name": data["genre"],
                                                                     "selectFields": fields_required,
                                                                     "notNullFields": ["name"]
                                                                     }
            response_movie_search: Dict[str, Optional[Any]] = api_request(url_movie_search_endswith,
                                                                          movie_search_params)
            if response_movie_search["docs"]:
                response_filtered_by_currency: List[Dict[str, Optional[Any]]] = list(
                    filter(lambda x: x["budget"]["currency"] == data["budget_currency"], response_movie_search["docs"]))
                response_movie_search["docs"]: List[Dict[str, Optional[Any]]] = response_filtered_by_currency
                data["pagination_info"]: Tuple[list, list] = get_pagination_data(response_movie_search)

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
