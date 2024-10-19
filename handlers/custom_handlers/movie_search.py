from loader import bot
from telebot.types import Message
from telebot.types import ReplyKeyboardRemove
from states.movie_search_states import MovieSearchState
from keyboards.reply.genres_reply_markup import genres_keyboard, genres_variants


@bot.message_handler(commands=['movie_search'])
def movie_by_name(message: Message) -> None:
    bot.set_state(message.from_user.id, MovieSearchState.name, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите название фильма или сериала:')


@bot.message_handler(state=MovieSearchState.name)
def get_movie_name(message: Message) -> None:
    movie_name_processed: str = message.text.strip()
    bot.set_state(message.from_user.id, MovieSearchState.genre, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = movie_name_processed
    bot.send_message(message.from_user.id, 'Хорошо. Теперь выберите жанр:', reply_markup=genres_keyboard)


@bot.message_handler(state=MovieSearchState.genre)
def get_movie_genre(message: Message) -> None:
    if message.text.lower() in genres_variants:
        bot.set_state(message.from_user.id, MovieSearchState.number_of_results, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['genre'] = message.text
        bot.send_message(message.from_user.id,
                         'Отлично! Сколько результатов вывести на экран?',
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.from_user.id, 'Выберите жанр из предложенных ниже:')


@bot.message_handler(state=MovieSearchState.number_of_results)
def get_number_of_options(message: Message) -> None:
    try:
        number_of_results = int(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['number_of_results'] = number_of_results
    except ValueError:
        bot.reply_to(message, 'Ошибка - введенное значение должно быть числом.\nСколько результатов вывести на экран?')


