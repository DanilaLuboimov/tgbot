from loader import bot
from typing import Callable
from keyboards.reply.default_keyboard import user_keyboard
from loguru import logger


def ex_log(func: Callable) -> Callable:
    """
    Декоратор для логирования исключений в обработчиках

    :param func: обработчик
    :type func: Callable
    :return: Callable
    """
    logger.add("debug.log", format="\n{time} [{level}]\n{message}",
               level="DEBUG")

    def wrapper(*args, **kwargs) -> None:
        try:
            result = func(*args, **kwargs)
        except Exception:
            bot.send_message(chat_id=args[0].chat.id,
                             text="<b>Что-то пошло не так!</b>\n"
                                  "Поиск прервался. Придется начать сначала.",
                             parse_mode="html", reply_markup=user_keyboard())
            bot.delete_state(user_id=args[0].from_user.id,
                             chat_id=args[0].chat.id)
            logger.exception("What?!")
        else:
            return result

    return wrapper
