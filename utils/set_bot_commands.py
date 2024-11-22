from telebot import TeleBot
from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot: TeleBot) -> None:
    """
    Set default commands for telegram bot.

    :param bot: telegram bot instance
    :type bot: TeleBot
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
