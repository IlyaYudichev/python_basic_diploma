from telebot.handler_backends import BaseMiddleware
from loader import bot
from config_data.config import DEFAULT_COMMANDS


class DeleteStateMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.update_types = ["message"]
        super().__init__()

    def pre_process(self, message, data):
        if message.text.startswith("/"):
            command_for_check: str = message.text.lstrip("/")
            for i_command in DEFAULT_COMMANDS:
                if i_command[0] == command_for_check:
                    bot.delete_state(message.from_user.id, message.chat.id)

    def post_process(self, message, data, exception) -> None:
        pass
