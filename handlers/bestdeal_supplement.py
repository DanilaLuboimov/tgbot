from loader import bot
from states.user_information import UserInfoState
from telebot.types import Message
from keyboards.reply.number_of_hotels import number_of_hotels
from utils.logging import ex_log


@bot.message_handler(state=UserInfoState.price_min)
@ex_log
def get_price(message: Message) -> None:
    """
    Обработчик устанавливает минимальную и максимальную
    цену за ночь в отелях

    :param message: Сообщение от пользователя
    :type message: Message
    :return: None
    """
    if message.text.isdigit():
        with bot.retrieve_data(user_id=message.from_user.id,
                               chat_id=message.chat.id) as data:
            if "price_min" not in data.keys():
                answer = "Введите <b><u>максимальную цену</u></b>," \
                         " за ночь в отеле, в долларах"
                data["price_min"] = message.text

                bot.set_state(message.from_user.id,
                              UserInfoState.price_min,
                              message.chat.id)
            else:
                answer = f"Введите <b><u>минимальное расстояние</u></b>" \
                         f" до центра города, в километрах"
                data["price_max"] = message.text

                bot.set_state(message.from_user.id,
                              UserInfoState.distance_min,
                              message.chat.id)
    else:
        answer = "<b>В сообщении должны быть только цифры!</b>"

    bot.send_message(chat_id=message.chat.id, text=answer,
                     parse_mode='html')


@bot.message_handler(state=UserInfoState.distance_min)
@ex_log
def get_distance(message: Message) -> None:
    """
    Обработчик устанавливает минимальную и максимальную дистанцию
    от отелей до центра города

    :param message: Сообщение от пользователя
    :type message: Message
    :return: None
    """
    if message.text.isdigit():
        with bot.retrieve_data(user_id=message.from_user.id,
                               chat_id=message.chat.id) as data:
            if "distance_min" not in data.keys():
                answer = f"Введите <b><u>максимальное расстояние</u></b>" \
                         f" до центра города, в километрах"
                data["distance_min"] = message.text

                bot.set_state(message.from_user.id,
                              UserInfoState.distance_min,
                              message.chat.id)

                bot.send_message(chat_id=message.chat.id, text=answer,
                                 parse_mode='html')
            else:
                answer = f"Сколько отелей показать?"
                data["distance_max"] = message.text

                bot.set_state(message.from_user.id,
                              UserInfoState.count_hotels,
                              message.chat.id)

                bot.send_message(chat_id=message.chat.id, text=answer,
                                 parse_mode='html',
                                 reply_markup=number_of_hotels())
    else:
        answer = "<b>В сообщении должны быть только цифры!</b>"

        bot.send_message(chat_id=message.chat.id, text=answer,
                         parse_mode='html')
