from telebot.types import ReplyKeyboardMarkup


def one_word_answer() -> ReplyKeyboardMarkup:
    """
    Функция создает клавиатуру для односложного ответа пользователя

    :return: ReplyKeyboardMarkup
    """
    user_answer = ["Да", "Нет"]

    answer = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 row_width=2)

    answer.add(*user_answer)

    return answer
