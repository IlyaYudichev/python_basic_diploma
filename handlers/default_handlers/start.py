from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    message_start: str = ("Я - бот-помощник в поиске фильмов. Помогу найти интересующие вас фильмы и сериалы "
                          "на просторах сайта kinopoisk.ru.\nЧтобы увидеть полный список моих функций, напишите"
                          " или выберете в меню /help»")

    bot.reply_to(message, f"Здравствуйте, {message.from_user.full_name}!\n{message_start}")
