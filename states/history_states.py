from telebot.handler_backends import State, StatesGroup


class HistoryStates(StatesGroup):
    """
    Class containing user states for "history" command.  Parent: StatesGroup.

        Attributes:
            search_history_date(State): user state for history date request
    """
    search_history_date = State()
