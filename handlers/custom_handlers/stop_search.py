from telebot.types import Message, ReplyKeyboardRemove
from loader import bot


@bot.message_handler(commands=["stop_search"])
def stop_search_handler(message: Message) -> None:
    """
    Stop search and delete user state.

    :param message: message from user
    :type message: Message
    """
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, "Поиск завершён.", reply_markup=ReplyKeyboardRemove())
