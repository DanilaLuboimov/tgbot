from loader import bot
from telebot.types import Message
from keyboards.reply.default_keyboard import user_keyboard
from keyboards.inline.hotel_website import hotel_website
from database.db_history import get_history_result, get_search_query
from utils.logging import ex_log


@bot.message_handler(commands=["history"])
@ex_log
def history(message: Message) -> None:
    """
    Функция отправляет пользователю сообщения с его историей

    :param message: Сообщение от пользователя
    :type message: Message
    :return: None
    """
    db_search_list = get_search_query(user_id=message.from_user.id)

    if len(db_search_list) == 0:
        answer = f"Вы еще <u>ничего</u> не искали!"
        bot.send_message(message.chat.id, answer, parse_mode='html',
                         reply_markup=user_keyboard())
    else:
        answer = f"<b>История поиска отелей:</b>"
        bot.send_message(message.chat.id, answer, parse_mode='html')

        for query in db_search_list:
            history_answer = f"Вы использовали команду: <u>{query[0]}</u>\n" \
                             f"Дата и время поиска: <b>{query[1]}</b>"
            result = get_history_result(user_id=message.from_user.id,
                                        search_id=query[2])

            if result[0][0] is None:
                history_answer += f"\n<b>Поиск не дал результатов</b>"
                bot.send_message(message.chat.id, history_answer,
                                 parse_mode='html')
            else:
                bot.send_message(message.chat.id, history_answer,
                                 parse_mode='html',
                                 reply_markup=hotel_website(result))

        answer = f"<b>Это вся ваша история поиска</b>"
        bot.send_message(message.chat.id, answer, parse_mode='html',
                         reply_markup=user_keyboard())
