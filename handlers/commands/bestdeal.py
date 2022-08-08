from loader import bot
from states.user_information import UserInfoState
from telebot.types import Message
from utils.logging import ex_log


@bot.message_handler(commands=["bestdeal"])
@ex_log
def bestdeal(message: Message) -> None:
    """
    Функция запускает череду обработчиков для поиска
    "По лучшему предложение"

    :param message: сообщение от пользователя
    :type message: Message
    :return: None
    """
    bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)

    answer = f"В какой <b>город</b> отправляемся?"

    bot.set_state(user_id=message.from_user.id, state=UserInfoState.city_name,
                  chat_id=message.chat.id)
    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode="html")
    with bot.retrieve_data(user_id=message.from_user.id,
                           chat_id=message.chat.id) as data:
        data["user_id"] = message.from_user.id
        data["user_filter"] = "DISTANCE_FROM_LANDMARK"
        data["command"] = message.text
        data["date"] = message.date
