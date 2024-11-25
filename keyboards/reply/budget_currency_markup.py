from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_budget_currency_markup() -> ReplyKeyboardMarkup:
    """
    Get budget currencies keyboard markup.

    :return: keyboard with buttons of available budget currencies
    :rtype: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_ruble = KeyboardButton("₽ (рубли)")
    button_dollar = KeyboardButton("$ (доллары)")
    button_euro = KeyboardButton("€ (евро)")
    keyboard.add(button_ruble, button_dollar, button_euro)
    return keyboard
