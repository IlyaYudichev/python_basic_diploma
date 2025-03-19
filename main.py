from loader import bot
from telebot.custom_filters import StateFilter
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from middleware.delete_state_middleware import DeleteStateMiddleware

if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.setup_middleware(DeleteStateMiddleware())
    bot.infinity_polling()
