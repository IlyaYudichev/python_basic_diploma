import operator
from typing import List, Tuple

from telebot.types import Message, CallbackQuery
from datetime import datetime

from database.common.models import History, db
from database.core import db_read, db_update
from loader import bot
from states.history_sates import HistoryStates
from utils.pagination_data import get_pagination_data
from utils.result_message import send_result_message

DATE_FORMAT: str = "%d.%m.%Y"
HISTORY_REQUEST: bool = True


@bot.message_handler(commands=["history"])
def request_for_date_of_history(message: Message) -> None:
    """
    Request for date for history of movie search.

    :param message: message from user
    :type message: Message
    """
    bot.set_state(message.from_user.id, HistoryStates.search_history_date, message.chat.id)
    bot.send_message(message.chat.id,
                     "За какую дату показать результаты поиска?\nВведите дату в формате ДД.ММ.ГГГГ:")


@bot.message_handler(state=HistoryStates.search_history_date)
def get_date_of_history_and_send_result(message: Message) -> None:
    """
    Convert date and send message with history of movie search.

    :param message: message from user
    :type message: Message
    """
    user_input_date: str = message.text
    try:
        date_of_history: datetime = datetime.strptime(user_input_date, DATE_FORMAT)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["date_of_history"]: datetime = date_of_history
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат даты.\nВведите дату в формате ДД.ММ.ГГГГ:")
        return
    date_required: bool = operator.eq(History.created_ad, date_of_history)
    user_id_required: bool = operator.eq(History.user_id, message.from_user.id)
    condition_required: bool = operator.and_(date_required, user_id_required)
    db_response = list(db_read(db, History, condition_required))
    if not db_response:
        bot.send_message(message.chat.id,
                         "В указанный день запросов не было.\nПопробуйте выбрать другую дату (ДД.ММ.ГГГГ):")
        return
    bot.send_message(message.chat.id, "Ожидайте, загружаем историю поиска...")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["pagination_info"]: Tuple[List[str], List[str]] = get_pagination_data(db_response, HISTORY_REQUEST)
        data["history_message_flag"]: bool = True
    send_result_message(message.from_user.id, message.chat.id)


@bot.callback_query_handler(
    func=lambda callback: callback.data.startswith("seen") or callback.data.startswith("unseen"))
def update_movie_status_and_send_result(callback: CallbackQuery) -> None:
    """
    Change movie status to seen or unseen and send message with history of movie search.

    :param callback: callback for change movie status
    :type callback: CallbackQuery
    """
    fields_to_update = dict()
    status_new: str = callback.data.split("_")[0]
    film_id: int = int(callback.data.split("_")[1])
    page_current: int = int(callback.data.split("_")[2])
    if status_new == "seen":
        fields_to_update["is_viewed"]: bool = True
    else:
        fields_to_update["is_viewed"]: bool = False
    film_id_required: bool = operator.eq(History.id, film_id)
    user_id_required: bool = operator.eq(History.user_id, callback.from_user.id)
    condition_for_update: bool = operator.and_(film_id_required, user_id_required)
    db_update(db, History, fields_to_update, condition_for_update)
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        date_of_history: datetime = data["date_of_history"]
    date_required: bool = operator.eq(History.created_ad, date_of_history)
    condition_for_read: bool = operator.and_(date_required, user_id_required)
    db_response = list(db_read(db, History, condition_for_read))
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        data["pagination_info"]: Tuple[List[str], List[str]] = get_pagination_data(db_response, HISTORY_REQUEST)
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    send_result_message(callback.from_user.id, callback.message.chat.id, page_current)
