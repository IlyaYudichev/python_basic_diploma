from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    """
    Send reply echo message to user.

    :param message: message from user
    :type message: Message
    """
    bot.reply_to(
        message,
        f"Эхо без состояния или фильтра.\nСообщение: {message.text}\nЧтобы увидеть полный список функций выберите в меню /help"
    )
