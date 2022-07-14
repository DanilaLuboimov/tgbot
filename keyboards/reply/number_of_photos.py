from telebot.types import ReplyKeyboardMarkup


def number_of_photos() -> ReplyKeyboardMarkup:
    user_answer = ["1", "2", "3", "4", "5", "6"]

    number = ReplyKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True,
                                        row_width=2)

    number.add(*user_answer)

    return number