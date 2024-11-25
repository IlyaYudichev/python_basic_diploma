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
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.startswith("/low"):
            data["kind_of_budget"]: str = "максимально"
        else:
            data["kind_of_budget"]: str = "минимально"
    bot.set_state(message.from_user.id, MovieByBudgetStates.budget_currency, message.chat.id)
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
        bot.set_state(message.from_user.id, MovieByBudgetStates.budget_value, message.chat.id)
        bot.send_message(message.chat.id,
                         f"Хорошо. Теперь введите {data["kind_of_budget"]} возможный бюджет для поиска",
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, "Ошибка. Выберите валюту бюджета из предложенных ниже:")


@bot.message_handler(state=MovieByBudgetStates.budget_value)
def get_budget_value(message: Message) -> None:
    if message.text.isdecimal():
