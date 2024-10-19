from telebot.handler_backends import State, StatesGroup


class MovieSearchState(StatesGroup):
    name = State()
    genre = State()
    number_of_results = State()
