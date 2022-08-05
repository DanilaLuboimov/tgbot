from telebot.types import ReplyKeyboardMarkup


def user_keyboard() -> ReplyKeyboardMarkup:
    """
    Функция создает клавиатуру с командами для бота

    :return: ReplyKeyboardMarkup
    """
    start_buttons = ["/lowprice", "/highprice", "/bestdeal", "/history",
                     "/help"]
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True,
                                   resize_keyboard=True, selective=True)
    keyboard.add(*start_buttons)
    return keyboard
