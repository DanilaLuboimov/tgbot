from telebot.types import ReplyKeyboardMarkup


def number_of_hotels() -> ReplyKeyboardMarkup:
    user_answer = ["1", "2", "3", "4", "5"]

    select_answer = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        row_width=3)

    select_answer.add(*user_answer)

    return select_answer
