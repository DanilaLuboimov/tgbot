from collections.abc import Callable
from telebot import types
from deep_translator import GoogleTranslator
from re import sub

import telebot
import requests
import json
import datetime

bot = telebot.TeleBot("5505382281:AAH2C8uRNQm5vfMkcwpD9o2QUVoEb8L7HfU")


def ex_wrapper(handler: Callable) -> Callable:
    def wrapped(message: types.Message, *args, **kwargs) -> None:
        try:
            handler(message, *args, **kwargs)
        except Exception:
            answer = "<b>Произошла ошибка!!!</b>"
            bot.send_message(chat_id=message.chat.id, text=answer,
                             parse_mode="html", reply_markup=user_keyboard())

    return wrapped


def user_keyboard() -> types.ReplyKeyboardMarkup:
    start_buttons = ["/lowprice", "/highprice", "/bestdeal", "/history",
                     "/help"]
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                         resize_keyboard=True)
    keyboard.add(*start_buttons)
    return keyboard


def info() -> str:
    text = f"<b>● /lowprice</b> — вывод самых дешёвых отелей в городе,\n" \
           f"<b>● /highprice</b> — вывод самых дорогих отелей в городе,\n" \
           f"<b>● /bestdeal</b> — вывод отелей, наиболее подходящих по цене и расположению от центра,\n" \
           f"<b>● /history</b> — вывод истории поиска отелей."
    return text


@bot.message_handler(commands=["start"])
@ex_wrapper
def start(message: types.Message) -> None:
    answer = f"Привет, {message.from_user.first_name}! Вот что я умею:\n{info()}"
    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode='html',
                     reply_markup=user_keyboard())


@bot.message_handler(commands=["lowprice", "highprice", "bestdeal"])
@ex_wrapper
def lowprice(message: types.Message) -> None:
    if message.text == "/lowprice":
        user_filter = "PRICE"
    elif message.text == "/highprice":
        user_filter = "PRICE_HIGHEST_FIRST"
    elif message.text == "/bestdeal":
        user_filter = "DISTANCE_FROM_LANDMARK"

    answer = f"В какой <b>город</b> отправляемся?"

    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode="html")
    types.ReplyKeyboardRemove(selective=True)
    bot.register_next_step_handler(message=message, callback=city,
                                   user_filter=user_filter)


@ex_wrapper
def city(message: types.Message, user_filter: str) -> None:
    bot.send_message(chat_id=message.chat.id, text="Начинаю искать город...",
                     parse_mode="html")

    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    headers = {
        "X-RapidAPI-Key": "1af874cea9msh6ce809ad8b501c7p1dc177jsn89961f5d0fb7",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    alphabet_ru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    name_city = message.text

    for letter in message.text.lower():
        if letter in alphabet_ru:
            name_city = GoogleTranslator(source='auto', target='en').translate(
                message.text.title())
            break

    querystring = {"query": name_city.lower(), "locale": "en_US",
                   "currency": "USD"}
    response = requests.request("GET", url, headers=headers,
                                params=querystring)

    data = json.loads(response.text)

    for i in data["suggestions"]:
        if len(i["entities"]) > 0:
            city_id = i["entities"][0]["destinationId"]
            break

    try:
        print(f"ID искомого города: {city_id}")
        answer = f"Нашел, теперь необходимо определиться с датами.\n" \
                 f"Например: {datetime.date.today()}\n" \
                 f"Впиши <u><b>дату въезда</b></u>"
        bot.send_message(chat_id=message.chat.id, text=answer,
                         parse_mode="html")
        bot.register_next_step_handler(message=message,
                                       callback=check_date,
                                       city_id=city_id,
                                       user_filter=user_filter)
    except Exception:
        answer = f"Не удалось найти такой город"
        bot.send_message(chat_id=message.chat.id, text=answer,
                         parse_mode="html",
                         reply_markup=user_keyboard())


@ex_wrapper
def check_date(message: types.Message, city_id: str, user_filter: str,
               counter: int = 1, check_in: str = None) -> None:
    dates_tuple = ("%d%m%y", "%d-%m-%y", "%d.%m.%y", "%d %m %y",
                   "%d%m%Y", "%d-%m-%Y", "%d.%m.%Y", "%d %m %Y",
                   "%y%m%d", "%y-%m-%d", "%y.%m.%d", "%y %m %d",
                   "%Y%m%d", "%Y-%m-%d", "%Y.%m.%d", "%Y %m %d")

    for form in dates_tuple:
        try:
            new_date = datetime.datetime.strptime(message.text, form)
        except Exception:
            continue
        else:
            new_date = datetime.date(year=new_date.year, month=new_date.month,
                                     day=new_date.day)
            break

    try:
        if counter == 1:
            check_in = new_date
            answer = f"Впиши <u><b>дату выезда</b></u>"
            bot.send_message(chat_id=message.chat.id, text=answer,
                             parse_mode='html')
            bot.register_next_step_handler(message=message,
                                           callback=check_date,
                                           counter=2,
                                           check_in=check_in,
                                           user_filter=user_filter,
                                           city_id=city_id
                                           )
        else:
            check_out = new_date
            user_answer = ["1", "2", "3", "4", "5"]
            select_answer = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                      one_time_keyboard=True,
                                                      row_width=3)
            select_answer.add(*user_answer)
            answer = f"<b>Сколько отелей показать?</b>"

            bot.send_message(chat_id=message.chat.id, text=answer,
                             parse_mode='html', reply_markup=select_answer)
            bot.register_next_step_handler(message=message,
                                           callback=count_hotel,
                                           check_in=check_in,
                                           check_out=check_out,
                                           user_filter=user_filter,
                                           city_id=city_id
                                           )
    except UnboundLocalError:
        bot.send_message(chat_id=message.chat.id, text="Указана неверная дата",
                         parse_mode='html', reply_markup=user_keyboard())


@ex_wrapper
def count_hotel(message: types.Message, check_in: str,
                check_out: str, user_filter: str, city_id: str) -> None:
    user_answer = ["Да", "Нет"]
    select_answer = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                              one_time_keyboard=True,
                                              row_width=2)
    select_answer.add(*user_answer)

    answer = f"<b>Выводить фотографии для каждого отеля?</b>"
    counter_hotels = message.text

    bot.send_message(chat_id=message.chat.id, text=answer,
                     parse_mode='html', reply_markup=select_answer)
    bot.register_next_step_handler(message=message,
                                   callback=print_photo,
                                   check_in=check_in,
                                   check_out=check_out,
                                   user_filter=user_filter,
                                   city_id=city_id,
                                   counter_hotels=counter_hotels
                                   )


@ex_wrapper
def print_photo(message: types.Message, check_in: str, counter_hotels: str,
                check_out: str, user_filter: str, city_id: str) -> None:
    try:
        if message.text.lower() == "да":
            user_answer = ["1", "2", "3", "4", "5", "6"]
            select_answer = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                      one_time_keyboard=True,
                                                      row_width=2)
            select_answer.add(*user_answer)
            answer = "Какое количество фотографий прикрепить?"
            bot.send_message(chat_id=message.chat.id, text=answer,
                             parse_mode='html', reply_markup=select_answer)
            bot.register_next_step_handler(message=message,
                                           callback=properties_list,
                                           check_in=check_in,
                                           check_out=check_out,
                                           user_filter=user_filter,
                                           city_id=city_id,
                                           counter_hotels=counter_hotels,
                                           )
        elif message.text.lower() == "нет":
            bot.register_next_step_handler(message=message,
                                           callback=properties_list(
                                               message=message,
                                               check_in=check_in,
                                               check_out=check_out,
                                               user_filter=user_filter,
                                               city_id=city_id,
                                               counter_hotels=counter_hotels,
                                           )
                                           )

        else:
            raise Exception
    except Exception:
        answer = "<b>Я тебя не понял</b>"
        bot.send_message(chat_id=message.chat.id, text=answer,
                         parse_mode='html', reply_markup=user_keyboard())


@ex_wrapper
def properties_list(message: types.Message, check_in: str,
                    user_filter: str, city_id: str, check_out: str,
                    counter_hotels: str,
                    price_min: str = "0", price_max: str = "5000") -> None:
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {
        "destinationId": city_id,
        "pageNumber": "1",
        "pageSize": "25",
        "checkIn": check_in,
        "checkOut": check_out,
        "adults1": "1",
        "priceMin": price_min,
        "priceMax": price_max,
        "sortOrder": user_filter,
        "locale": "en_US",
        "currency": "USD",
        "accommodationIds": "12,1"
    }

    headers = {
        "X-RapidAPI-Key": "1af874cea9msh6ce809ad8b501c7p1dc177jsn89961f5d0fb7",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers,
                                params=querystring)
    j = json.loads(response.text)
    my_list = list()

    for i in j["data"]["body"]["searchResults"]["results"]:
        my_list.append([i["name"],
                        i["ratePlan"]["price"]["fullyBundledPricePerStay"][
                        7::],
                        str(i["id"]),
                        i["address"]["streetAddress"],
                        i["landmarks"][0]["distance"]
                        ])

    for mess in my_list[:int(counter_hotels):]:
        markup = types.InlineKeyboardMarkup()
        hotel_site = types.InlineKeyboardButton(text=mess[0],
                                                url=f"https://www.hotels.com/ho{mess[2]}/?q-check-in={check_in}&q-check-out={check_out}&q-rooms=1&q-room-0-adults=1&q-room-0-children=0&f-hotel-id={mess[2]}")
        markup.add(hotel_site)

        if message.text.isdigit() and int(message.text) in range(1, 7):
            url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

            querystring = {"id": f"{mess[2]}"}

            response = requests.request("GET", url, headers=headers,
                                        params=querystring)
            photo_json = json.loads(response.text)
            photo_list = list()

            for p in photo_json["hotelImages"][:int(message.text):]:
                photo = sub(r"{size}", r"z", p["baseUrl"])
                hotel_photo = types.InputMediaPhoto(photo)
                photo_list.append(hotel_photo)

            bot.send_media_group(chat_id=message.chat.id, media=photo_list)

        answer = f"Название отеля: {mess[0]}\n" \
                 f"Адрес: {mess[3]}\n" \
                 f"До центра города: {mess[4]}\n" \
                 f"Цена: ${mess[1]}"
        bot.send_message(chat_id=message.chat.id, text=answer,
                         parse_mode="html",
                         reply_markup=markup)

    answer = "Это все, что я могу предложить по твоему запросу"
    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode="html",
                     reply_markup=user_keyboard())


@bot.message_handler(commands=["history"])
@ex_wrapper
def history(message: types.Message) -> None:
    answer = f"<b>История поиска отелей</b>"
    bot.send_message(message.chat.id, answer, parse_mode='html',
                     reply_markup=user_keyboard())
    types.ReplyKeyboardRemove(selective=True)


@bot.message_handler(commands=["help"])
@ex_wrapper
def help(message: types.Message) -> None:
    answer = info()
    bot.send_message(message.chat.id, answer, parse_mode='html',
                     reply_markup=user_keyboard())


@bot.message_handler(content_types=["text"])
@ex_wrapper
def another_message(message: types.Message) -> None:
    answer = "<b>Я тебя не понимаю, воспользуйся <u>/help</u></b>"
    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode='html',
                     reply_markup=user_keyboard())


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
