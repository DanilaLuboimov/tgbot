from loader import bot
from states.user_information import UserInfoState
from utils.calendar import get_calendar
from utils.logging import ex_log
from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from api_request import city, photo, properties
from keyboards.reply.default_keyboard import user_keyboard
from keyboards.reply.number_of_hotels import number_of_hotels
from keyboards.reply.one_word_answer import one_word_answer
from keyboards.reply.number_of_photos import number_of_photos
from keyboards.inline.hotel_website import hotel_website
from datetime import date, timedelta, datetime
from database.create_a_new_search_query import new_search_query
from database.create_new_results import new_results


@bot.message_handler(state=UserInfoState.city_name)
@ex_log
def get_city_name(message: Message) -> None:
    """
    Обработчик определяет название города и его id,
    по запросу пользователя и просит подтверждение

    :param message: Сообщение от пользователя
    :type message: Message
    :return: None
    """
    bot.send_message(chat_id=message.chat.id, text="Начинаю искать город...",
                     parse_mode="html")

    try:
        city_id, city_name = city.get_city(message_text=message.text)
    except TypeError:
        bot.send_message(chat_id=message.chat.id,
                         text=f'Не получилось найти город '
                              f'<u>"{message.text}"</u>\n'
                              f'Попробуйте другой',
                         parse_mode="html")
    else:
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
@ex_log
def create_date(message: Message) -> None:
    """
    Обработчик, при утвердительном ответе пользователя,
    создает клавиатуру для ввода даты, иначе возвращается
    к get_city_name

    :param message: Сообщение от пользователя
    :type message: Message
    :return: None
    """
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
    elif message.text.lower() == "нет":
        text = "Попробуйте ввести <b>другой</b> город"

        bot.set_state(user_id=message.from_user.id,
                      state=UserInfoState.city_name,
                      chat_id=message.chat.id)
        bot.send_message(chat_id=message.chat.id,
                         text=text, parse_mode="html")
    else:
        bot.send_message(chat_id=message.chat.id,
                         text="Требуется ответ <b><u>Да/Нет</u></b>",
                         parse_mode="html",
                         reply_markup=one_word_answer())


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
@ex_log
def create_date(call: CallbackQuery) -> None:
    """
    Обработчик определяет даты въезда и выезда из отелей,
    заданные пользователем с помощью встроенной клавиатуры

    :param call: Запрос обратного вызова
    :type call: CallbackQuery
    :return:
    """
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

                if "price_min" not in data.keys():
                    answer = "Введите <b><u>минимальную цену</u></b>," \
                             " за ночь в отеле, в долларах"

                    bot.set_state(call.from_user.id,
                                  UserInfoState.price_min,
                                  call.message.chat.id)

                    bot.send_message(chat_id=call.message.chat.id, text=answer,
                                     parse_mode='html')
                else:
                    answer = f"Сколько отелей показать?"

                    bot.set_state(call.from_user.id,
                                  UserInfoState.count_hotels,
                                  call.message.chat.id)

                    bot.send_message(chat_id=call.message.chat.id, text=answer,
                                     parse_mode='html',
                                     reply_markup=number_of_hotels())


@bot.message_handler(state=UserInfoState.count_hotels)
@ex_log
def count_hotel(message: Message) -> None:
    """
    Обработчик устанавливает значение по количеству отелей в результате
    выдаче пользователю

    :param message: Сообщение от пользователя
    :type message: Message
    :return: None
    """
    answer = f"Выводить фотографии для каждого отеля?"

    with bot.retrieve_data(user_id=message.from_user.id,
                           chat_id=message.chat.id) as data:
        data["count_hotels"] = message.text

    bot.set_state(message.from_user.id, UserInfoState.need_photos,
                  message.chat.id)

    bot.send_message(chat_id=message.chat.id, text=answer,
                     parse_mode='html', reply_markup=one_word_answer())


@bot.message_handler(state=UserInfoState.need_photos)
@ex_log
def print_photo(message: Message) -> None:
    """
    Обработчик устанавливает значение о необходимости прикреплять
    фотографии к результатам в выдаче пользователю

    :param message: Сообщение от пользователя
    :type message: Message
    :return: None
    """
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
@ex_log
def properties_list(message: Message) -> None:
    """
    Обработчик предоставляет пользователю результат поиска отелей
    по заданным ранее параметрам

    :param message: Сообщение от пользователя
    :type message: Message
    :return: None
    """
    bot.send_message(chat_id=message.chat.id, text="Начинаю поиск отелей...",
                     parse_mode='html')

    with bot.retrieve_data(user_id=message.from_user.id,
                           chat_id=message.chat.id) as data:
        city_name = data["city_name"]
        city_id = data["city_id"]
        check_in = data["check_in"]
        check_out = data["check_out"]
        price_min = data["price_min"]
        price_max = data["price_max"]
        user_filter = data["user_filter"]

    if data["user_filter"] == "DISTANCE_FROM_LANDMARK":
        landmark_ids = data["city_id"]
        distance_min = float(data["distance_min"])
        distance_max = float(data["distance_max"])
        hotels_list = properties.get_properties(city_id, check_in,
                                                check_out,
                                                price_min,
                                                price_max,
                                                user_filter,
                                                city_name,
                                                landmark_ids,
                                                distance_min,
                                                distance_max,
                                                )
    else:
        hotels_list = properties.get_properties(city_id, check_in,
                                                check_out,
                                                price_min,
                                                price_max,
                                                user_filter,
                                                city_name)

    db_hotels_result = list()

    for hotel in hotels_list[:int(data["count_hotels"]):]:
        if message.text.isdigit() and int(message.text) in range(1, 7):
            data["count_photos"] = message.text

            photos = photo.get_photos(hotel_id=hotel[2],
                                      count=int(data["count_photos"]))

            bot.send_media_group(chat_id=message.chat.id,
                                 media=photos)

        if hotel[5] == 1:
            nights = "ночь"
        elif 2 <= hotel[5] >= 4:
            nights = "ночи"
        else:
            nights = "ночей"

        answer = f"Название отеля: {hotel[0]}\n" \
                 f"Адрес: {hotel[3]}\n" \
                 f"{hotel[4]}\n" \
                 f"Цена за {hotel[5]} {nights}: <b>${hotel[1]}</b>"

        if nights != "ночь":
            hotel[1] = hotel[1].replace(",", "", 1)
            price = round(float(hotel[1]) / hotel[5], 2)
            if str(price).endswith(".0"):
                price = str(price)[:-2:]
            answer += f"\nЦена за ночь: <b>${price}</b>"

        url = f"https://www.hotels.com/ho{hotel[2]}/?q-check-in={check_in}&q-check-out={check_out}&q-rooms=1&q-room-0-adults=1&q-room-0-children=0&f-hotel-id={hotel[2]}"

        db_hotels_result.append((url, hotel[0]))

        bot.send_message(chat_id=message.chat.id, text=answer,
                         parse_mode="html",
                         reply_markup=hotel_website(hotels=[(url, hotel[0])])
                         )

    search_id_from_db = new_search_query(command=data["command"],
                                         date_time=data["date"],
                                         fk_user_id=data["user_id"])

    if len(hotels_list) == 0:
        answer = "К сожалению по вашему запросу не удалось найти отелей"
        new_results(search_id=search_id_from_db)
    else:
        answer = "Это все, что я могу предложить по вашему запросу"

        for result in db_hotels_result:
            new_results(search_id=search_id_from_db,
                        hotel_url=result[0], hotel_name=result[1])

    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode="html",
                     reply_markup=user_keyboard())

    bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
