from random import choice
from typing import Tuple

from telebot.types import Message
from loader import bot


@bot.message_handler(regexp=r'\bдобр')
@bot.message_handler(regexp=r'\bздравствуй')
@bot.message_handler(regexp=r'\bпр[ие]вет')
def greetings(message: Message) -> None:
    """
    Send reply greetings message to user.

    :param message: message from user
    :type message: Message
    """
    greeting_variants: Tuple[str, ...] = ('Привет', 'Здравствуйте', 'Доброго времени суток')
    greeting_message: str = ('Давайте подберём вам фильм или сериал на сайте kinopoisk.ru! '
                             '\nЧтобы увидеть полный список моих функций, напишите или выберите в меню /help')

    greeting_random: str = choice(greeting_variants)
    bot.reply_to(message, f"{greeting_random}, {message.from_user.first_name}!\n{greeting_message}")
