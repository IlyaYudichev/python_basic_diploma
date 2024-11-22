from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['hello_world'])
def test_command(message: Message) -> None:
    """
    Test command.

    :param message: message from user
    :type message: Message
    """
    bot.reply_to(message, 'Привет, мир!!!')
