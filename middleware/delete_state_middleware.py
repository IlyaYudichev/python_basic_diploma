from telebot.handler_backends import BaseMiddleware
from telebot.types import Message

from loader import bot
from config_data.config import DEFAULT_COMMANDS


class DeleteStateMiddleware(BaseMiddleware):
    """Class that allows to start new command while handling another command. Parent: BaseMiddleware."""

    def __init__(self) -> None:
        self.update_types = ["message"]
        super().__init__()

    def pre_process(self, message: Message, data: dict) -> None:
        """
        Delete user state and start handling new command if user message is bot command.

        :param message: message from user
        :type message: Message
        :param data: data for handling user command
        :type data: dict
        """
        if message.text.startswith("/"):
            command_for_check: str = message.text.lstrip("/")
            for i_command in DEFAULT_COMMANDS:
                if i_command[0] == command_for_check:
                    bot.delete_state(message.from_user.id, message.chat.id)

    def post_process(self, message, data, exception) -> None:
        pass
