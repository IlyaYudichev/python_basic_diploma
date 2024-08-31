from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['hello_world'])
def test_command(message: Message) -> None:
    bot.reply_to(message, 'Привет, мир!!!')
