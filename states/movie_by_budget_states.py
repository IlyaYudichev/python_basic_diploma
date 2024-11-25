from telebot.handler_backends import State, StatesGroup


class MovieByBudgetStates(StatesGroup):
    """
    Class containing user states for "low_budget_movie" and "high_budget_movie" commands.  Parent: StatesGroup.

        Attributes:
            budget_currency (State): user state for budget currency request
            budget_value (State): user state for budget value request
            genre (State): user state for movie genre request
            number_of_results (State): user state for request for number of results
    """
    budget_currency = State()
    budget_value = State()
    genre = State()
    number_of_results = State()
