from loader import bot
from states.user_information import UserInfoState
from utils.calendar import get_calendar
from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from api_request import city, photo, properties
from keyboards.reply.default_keyboard import user_keyboard
from keyboards.reply.number_of_hotels import number_of_hotels
from keyboards.reply.one_word_answer import one_word_answer
from keyboards.reply.number_of_photos import number_of_photos
from keyboards.inline.hotel_website import hotel_website
from datetime import date, timedelta, datetime


@bot.message_handler(state=UserInfoState.price_min)
def get_price(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(user_id=message.from_user.id,
                               chat_id=message.chat.id) as data:
            if "price_min" not in data.keys():
                answer = "Введите максимальную цену, за ночь в отеле," \
                         " в долларах"
                data["price_min"] = message.text

                bot.set_state(message.from_user.id,
                              UserInfoState.price_min,
                              message.chat.id)
            else:
                answer = f"Введите минимальное расстояние до центра " \
                         f"города, в километрах"
                data["price_max"] = message.text

                bot.set_state(message.from_user.id,
                              UserInfoState.distance_min,
                              message.chat.id)
    else:
        answer = "В сообщении должны быть только цифры"

    bot.send_message(chat_id=message.chat.id, text=answer,
                     parse_mode='html')


@bot.message_handler(state=UserInfoState.distance_min)
def get_distance(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(user_id=message.from_user.id,
                               chat_id=message.chat.id) as data:
            if "distance_min" not in data.keys():
                answer = f"Введите максимальное расстояние до центра " \
                         f"города, в километрах"
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
        answer = "В сообщении должны быть только цифры"

        bot.send_message(chat_id=message.chat.id, text=answer,
                         parse_mode='html')