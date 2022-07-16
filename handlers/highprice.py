from loader import bot
from states.user_information import UserInfoState
from utils.calendar import get_calendar
from telebot.types import Message, CallbackQuery, InputMediaPhoto
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from re import sub
from api_request import city, photos, properties
from keyboards.reply.default_keyboard import user_keyboard
from keyboards.reply.number_of_hotels import number_of_hotels
from keyboards.reply.one_word_answer import one_word_answer
from keyboards.reply.number_of_photos import number_of_photos
from keyboards.inline.hotel_website import hotel_website
from datetime import date, timedelta, datetime


@bot.message_handler(commands=["highprice"])
# @ex_wrapper
def highprice(message: Message) -> None:
    bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)

    answer = f"В какой <b>город</b> отправляемся?"

    bot.set_state(user_id=message.from_user.id, state=UserInfoState.city_name,
                  chat_id=message.chat.id)
    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode="html")
    with bot.retrieve_data(user_id=message.from_user.id,
                           chat_id=message.chat.id) as data:
        data["user_id"] = str(message.from_user.id)
        data["user_filter"] = "PRICE_HIGHEST_FIRST"
        data["price_min"] = "0"
        data["price_max"] = "5000"


@bot.message_handler(state=UserInfoState.city_name)
def get_city_name(message: Message) -> None:
    bot.send_message(chat_id=message.chat.id, text="Начинаю искать город...",
                     parse_mode="html")

    city_id, city_name = city.get_city(message_text=message.text)

    with bot.retrieve_data(user_id=message.from_user.id,
                           chat_id=message.chat.id) as data:
        data["city_name"] = city_name
        data["city_id"] = city_id

        answer = f"Нашел <b><u>{city_name}</u></b> по запросу\n" \
                 f"Требуется Ваше подтверждение"

        bot.set_state(user_id=message.from_user.id,
                      state=UserInfoState.check_in)
        bot.send_message(chat_id=message.chat.id, text=answer,
                         parse_mode="html", reply_markup=one_word_answer())


@bot.message_handler(state=UserInfoState.check_in)
def create_date(message: Message) -> None:
    try:
        if message.text.lower() == "да":

            calendar, step = get_calendar(is_process=False,
                                          current_date=date.today(),
                                          min_date=date.today(),
                                          locale="ru")
            if LSTEP[step] == "year":
                text = "Выберите год"

            bot.send_message(chat_id=message.chat.id,
                             text=text,
                             reply_markup=calendar)
        else:
            text = "Попробуйте ввести другой город"

            bot.set_state(user_id=message.from_user.id,
                          state=UserInfoState.city_name,
                          chat_id=message.chat.id)
            bot.send_message(chat_id=message.chat.id,
                             text=text)
    except Exception:
        pass


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def create_date(call: CallbackQuery) -> None:
    date_lower_limit = date.today()

    with bot.retrieve_data(user_id=call.from_user.id,
                           chat_id=call.message.chat.id) as data:
        if "check_out" not in data.keys() and "check_in" in data.keys():
            date_lower_limit = datetime.strptime(data["check_in"],
                                                 "%Y-%m-%d").date() + timedelta(
                days=1)

    result, key, step = get_calendar(is_process=True, callback_data=call.data,
                                     current_date=date_lower_limit,
                                     min_date=date_lower_limit, locale="ru")

    if not result and key:
        if LSTEP[step] == "month":
            text = "Выберите месяц"
        elif LSTEP[step] == "day":
            bot.set_state(user_id=call.from_user.id,
                          state=UserInfoState.check_out)
            text = "Выберите день"

        bot.edit_message_text(text=text,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=key)

    elif result:
        with bot.retrieve_data(user_id=call.from_user.id,
                               chat_id=call.message.chat.id) as data:
            if "check_in" not in data.keys():
                bot.edit_message_text(f"Ваша дата въезда {result}",
                                      call.message.chat.id,
                                      call.message.message_id)

                data["check_in"] = str(result)

                bot.set_state(user_id=call.from_user.id,
                              state=UserInfoState.check_in)

                date_lower_limit = datetime.strptime(
                    str(result),
                    "%Y-%m-%d").date() + timedelta(
                    days=1)

                calendar, step = get_calendar(is_process=False,
                                              current_date=date_lower_limit,
                                              min_date=date_lower_limit,
                                              locale="ru")

                if LSTEP[step] == "year":
                    text = "Выберите год"

                bot.send_message(chat_id=call.message.chat.id,
                                 text=text,
                                 reply_markup=calendar)

            elif "check_out" not in data.keys():
                bot.edit_message_text(f"Ваша дата выезда {result}",
                                      call.message.chat.id,
                                      call.message.message_id)

                data["check_out"] = str(result)

                answer = f"<b>Сколько отелей показать?</b>"

                bot.set_state(call.from_user.id,
                              UserInfoState.count_hotels,
                              call.message.chat.id)

                bot.send_message(chat_id=call.message.chat.id, text=answer,
                                 parse_mode='html',
                                 reply_markup=number_of_hotels())


@bot.message_handler(state=UserInfoState.count_hotels)
# @ex_wrapper
def count_hotel(message: Message) -> None:
    answer = f"<b>Выводить фотографии для каждого отеля?</b>"

    with bot.retrieve_data(user_id=message.from_user.id,
                           chat_id=message.chat.id) as data:
        data["count_hotels"] = message.text

    bot.set_state(message.from_user.id, UserInfoState.need_photos,
                  message.chat.id)

    bot.send_message(chat_id=message.chat.id, text=answer,
                     parse_mode='html', reply_markup=one_word_answer())


@bot.message_handler(state=UserInfoState.need_photos)
# @ex_wrapper
def print_photo(message: Message) -> None:
    if message.text.lower() == "да":
        with bot.retrieve_data(user_id=message.from_user.id,
                               chat_id=message.chat.id) as data:
            data["need_photos"] = message.text

        answer = "Какое количество фотографий прикрепить?"

        bot.set_state(message.from_user.id, UserInfoState.count_photos,
                      message.chat.id)
        bot.send_message(chat_id=message.chat.id, text=answer,
                         parse_mode='html', reply_markup=number_of_photos())

    elif message.text.lower() == "нет":
        with bot.retrieve_data(user_id=message.from_user.id,
                               chat_id=message.chat.id) as data:
            data["need_photos"] = message.text

        properties_list(message=message)


@bot.message_handler(state=UserInfoState.count_photos)
# @ex_wrapper
def properties_list(message: Message) -> None:
    hotels_json, data = properties.get_properties(message=message)
    hotel_list = list()

    for i in hotels_json["data"]["body"]["searchResults"]["results"]:
        hotel_list.append([i["name"],
                           i["ratePlan"]["price"][
                               "fullyBundledPricePerStay"][
                           7::],
                           str(i["id"]),
                           i["address"]["streetAddress"],
                           i["landmarks"][0]["distance"]
                           ])

    for hotel in hotel_list[:int(data["count_hotels"]):]:
        if message.text.isdigit() and int(message.text) in range(1, 7):
            data["count_photos"] = message.text

            photo_json = photos.get_photos(hotel_id=hotel[2])
            photo_list = list()

            for p in photo_json["hotelImages"][
                     :int(data["count_photos"]):]:
                photo = sub(r"{size}", r"z", p["baseUrl"])
                hotel_photo = InputMediaPhoto(photo)
                photo_list.append(hotel_photo)

            bot.send_media_group(chat_id=message.chat.id,
                                 media=photo_list)

        answer = f"Название отеля: {hotel[0]}\n" \
                 f"Адрес: {hotel[3]}\n" \
                 f"До центра города: {hotel[4]}\n" \
                 f"Цена: ${hotel[1]}"
        bot.send_message(chat_id=message.chat.id, text=answer,
                         parse_mode="html",
                         reply_markup=hotel_website(hotel_name=hotel[0],
                                                    hotel_id=hotel[2],
                                                    check_in=data["check_in"],
                                                    check_out=data["check_out"]
                                                    )
                         )

    answer = "Это все, что я могу предложить по вашему запросу"

    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode="html",
                     reply_markup=user_keyboard())

    # здесь будет добавлена функция для записи в БД

    bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
