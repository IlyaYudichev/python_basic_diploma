from telebot.handler_backends import State, StatesGroup


class MovieByRatingStates(StatesGroup):
    """
    Class containing user states for "movie_by_rating" command. Parent: StatesGroup.

        Attributes:
            rating (State): user state for movie rating request
            genre (State): user state for movie genre request
            number_of_results (State): user state for request for number of results
    """
    rating = State()
    genre = State()
    number_of_results = State()
