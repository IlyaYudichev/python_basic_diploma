from telebot.handler_backends import State, StatesGroup


class MovieSearchState(StatesGroup):
    """
    Class containing user states for "movie_search" command.  Parent: StatesGroup.

        Attributes:
            name (State): user state for movie name request
            genre (State): user state for movie genre request
            number_of_results (State): user state for request for number of results
    """
    name = State()
    genre = State()
    number_of_results = State()
