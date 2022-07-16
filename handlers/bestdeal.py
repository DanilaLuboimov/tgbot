# from loader import bot
# from states.user_information import UserInfoState
# from telebot import types
#
#
# # Еще не готово
# @bot.message_handler(commands=["bestdeal"])
# # @ex_wrapper
# def bestdeal(message: types.Message) -> None:
#     bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
#
#     answer = f"В какой <b>город</b> отправляемся?"
#
#     bot.set_state(user_id=message.from_user.id, state=UserInfoState.city_name,
#                   chat_id=message.chat.id)
#     bot.send_message(chat_id=message.chat.id, text=answer, parse_mode="html")
#     with bot.retrieve_data(user_id=message.from_user.id,
#                            chat_id=message.chat.id) as data:
#         data["user_id"] = str(message.from_user.id)
#         data["user_filter"] = "DISTANCE_FROM_LANDMARK"
#
#
# @bot.message_handler(state=UserInfoState.city_name)
# def get_city_name(message: types.Message) -> None:
#     bot.send_message(chat_id=message.chat.id, text="Начинаю искать город...",
#                      parse_mode="html")
#
#     url = "https://hotels4.p.rapidapi.com/locations/v2/search"
#
#     alphabet_ru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
#     name_city = message.text
#
#     for letter in message.text.lower():
#         if letter in alphabet_ru:
#             name_city = GoogleTranslator(source='auto', target='en').translate(
#                 message.text.title())
#             break
#
#     querystring = {"query": name_city.lower(), "locale": "en_US",
#                    "currency": "USD"}
#     response = requests.get(url=url, headers=headers,
#                             params=querystring, timeout=15)
#
#     if response.status_code == requests.codes.ok:
#         data = json.loads(response.text)
#
#         for i in data["suggestions"]:
#             if len(i["entities"]) > 0:
#                 city_id = i["entities"][0]["destinationId"]
#                 break
#
#         with bot.retrieve_data(user_id=message.from_user.id,
#                                chat_id=message.chat.id) as data:
#             data["city_name"] = message.text
#             data["city_id"] = city_id
#
#         answer = f"Нашел, теперь необходимо определиться с датами.\n"
#
#         bot.set_state(user_id=message.from_user.id,
#                       state=UserInfoState.check_in)
#         bot.send_message(chat_id=message.chat.id, text=answer,
#                          parse_mode="html")
#         bot.register_next_step_handler(message=message,
#                                        callback=check_date(message))
#         bot.clear_step_handler(message=message)
#
#
# @bot.message_handler(state=[UserInfoState.check_in, UserInfoState.check_out])
# def check_date(mess: types.Message, counter: int = 1) -> None:
#     lower_limit = date.today()
#     upper_limit = date.today()
#
#     for _ in range(3):
#         days_in_month = \
#             calendar.monthrange(upper_limit.year, upper_limit.month)[1]
#         upper_limit += timedelta(days=days_in_month)
#
#     if counter == 1:
#         text = "Выберите <b><u>дату въезда</u></b>"
#     else:
#         text = "Выберите <b><u>дату выезда</u></b>"
#
#     bot.send_message(chat_id=mess.chat.id, text=text,
#                      parse_mode="html")
#
#     calend, step = DetailedTelegramCalendar(min_date=lower_limit,
#                                             max_date=upper_limit,
#                                             locale="ru").build()
#
#     if LSTEP[step] == "year":
#         text = "Выберите год"
#
#     bot.send_message(chat_id=mess.chat.id,
#                      text=text,
#                      reply_markup=calend)
#
#     @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
#     def create_date(call: types.CallbackQuery):
#         lower_limit = date.today()
#         upper_limit = date.today()
#
#         for _ in range(3):
#             days_in_month = \
#                 calendar.monthrange(upper_limit.year, upper_limit.month)[1]
#             upper_limit += timedelta(days=days_in_month)
#
#         with bot.retrieve_data(user_id=call.from_user.id,
#                                chat_id=call.message.chat.id) as data:
#             if "check_out" not in data.keys() and "check_in" in data.keys():
#                 lower_limit = datetime.strptime(data["check_in"],
#                                                 "%Y-%m-%d").date() + timedelta(
#                     days=1)
#
#         result, key, step = DetailedTelegramCalendar(min_date=lower_limit,
#                                                      max_date=upper_limit,
#                                                      locale="ru").process(
#             call.data)
#
#         if not result and key:
#             if LSTEP[step] == "month":
#                 text = "Выберите месяц"
#             elif LSTEP[step] == "day":
#                 text = "Выберите день"
#
#             bot.edit_message_text(text=text,
#                                   chat_id=call.message.chat.id,
#                                   message_id=call.message.message_id,
#                                   reply_markup=key)
#
#         elif result:
#             with bot.retrieve_data(user_id=call.from_user.id,
#                                    chat_id=call.message.chat.id) as data:
#                 if "check_in" not in data.keys():
#                     bot.edit_message_text(f"Ваша дата въезда {result}",
#                                           call.message.chat.id,
#                                           call.message.message_id)
#
#                     data["check_in"] = str(result)
#
#                     bot.set_state(user_id=call.from_user.id,
#                                   state=UserInfoState.check_in)
#
#                     bot.register_next_step_handler(message=call.message,
#                                                    callback=check_date(mess,
#                                                                        counter=2)
#                                                    )
#                     bot.clear_step_handler(message=mess)
#                 elif "check_out" not in data.keys():
#                     bot.edit_message_text(f"Ваша дата выезда {result}",
#                                           call.message.chat.id,
#                                           call.message.message_id)
#
#                     data["check_out"] = str(result)
#
#                     answer = f"<b>Сколько отелей показать?</b>"
#
#                     bot.set_state(call.from_user.id,
#                                   UserInfoState.count_hotels,
#                                   call.message.chat.id)
#                     bot.send_message(chat_id=call.message.chat.id, text=answer,
#                                      parse_mode='html',
#                                      reply_markup=number_of_hotels())
#
#
# @bot.message_handler(state=UserInfoState.count_hotels)
# # @ex_wrapper
# def count_hotel(message: types.Message) -> None:
#     answer = f"<b>Выводить фотографии для каждого отеля?</b>"
#
#     with bot.retrieve_data(user_id=message.from_user.id,
#                            chat_id=message.chat.id) as data:
#         data["count_hotels"] = message.text
#
#     bot.set_state(message.from_user.id, UserInfoState.need_photos,
#                   message.chat.id)
#     bot.send_message(chat_id=message.chat.id, text=answer,
#                      parse_mode='html', reply_markup=one_word_answer())
#     bot.register_next_step_handler(message=message, callback=print_photo)
#
#
# # @ex_wrapper
# def print_photo(message: types.Message) -> None:
#     if message.text.lower() == "да":
#         with bot.retrieve_data(user_id=message.from_user.id,
#                                chat_id=message.chat.id) as data:
#             data["need_photos"] = message.text
#
#         answer = "Какое количество фотографий прикрепить?"
#
#         bot.send_message(chat_id=message.chat.id, text=answer,
#                          parse_mode='html', reply_markup=number_of_photos())
#         bot.register_next_step_handler(message=message,
#                                        callback=properties_list)
#     elif message.text.lower() == "нет":
#         with bot.retrieve_data(user_id=message.from_user.id,
#                                chat_id=message.chat.id) as data:
#             data["need_photos"] = message.text
#
#         bot.register_next_step_handler(message=message,
#                                        callback=properties_list(
#                                            message=message))
#         bot.clear_step_handler(message=message)
#
#
# # @ex_wrapper
# def properties_list(message: types.Message) -> None:
#     url = "https://hotels4.p.rapidapi.com/properties/list"
#
#     with bot.retrieve_data(user_id=message.from_user.id,
#                            chat_id=message.chat.id) as data:
#         city_id = data["city_id"]
#         check_in = data["check_in"]
#         check_out = data["check_out"]
#         price_min = data["price_min"]
#         price_max = data["price_max"]
#         user_filter = data["user_filter"]
#
#     querystring = {
#         "destinationId": city_id,
#         "pageNumber": "1",
#         "pageSize": "25",
#         "checkIn": check_in,
#         "checkOut": check_out,
#         "adults1": "1",
#         "priceMin": price_min,
#         "priceMax": price_max,
#         "sortOrder": user_filter,
#         "locale": "en_US",
#         "currency": "USD",
#         "accommodationIds": "12,1"
#     }
#
#     text = "Начинаю подбирать отели по запросу..."
#
#     bot.send_message(chat_id=message.chat.id, text=text)
#
#     response = requests.get(url=url, headers=headers,
#                             params=querystring, timeout=20)
#
#     if response.status_code == requests.codes.ok:
#
#         data_j = json.loads(response.text)
#         my_list = list()
#
#         for i in data_j["data"]["body"]["searchResults"]["results"]:
#             my_list.append([i["name"],
#                             i["ratePlan"]["price"][
#                                 "fullyBundledPricePerStay"][
#                             7::],
#                             str(i["id"]),
#                             i["address"]["streetAddress"],
#                             i["landmarks"][0]["distance"]
#                             ])
#
#         for mess in my_list[:int(data["count_hotels"]):]:
#
#             if message.text.isdigit() and int(message.text) in range(1, 7):
#                 data["count_photos"] = message.text
#                 url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
#
#                 querystring = {"id": f"{mess[2]}"}
#
#                 response = requests.request("GET", url, headers=headers,
#                                             params=querystring)
#                 photo_json = json.loads(response.text)
#                 photo_list = list()
#
#                 for p in photo_json["hotelImages"][
#                          :int(data["count_photos"]):]:
#                     photo = sub(r"{size}", r"z", p["baseUrl"])
#                     hotel_photo = types.InputMediaPhoto(photo)
#                     photo_list.append(hotel_photo)
#
#                 bot.send_media_group(chat_id=message.chat.id,
#                                      media=photo_list)
#
#             answer = f"Название отеля: {mess[0]}\n" \
#                      f"Адрес: {mess[3]}\n" \
#                      f"До центра города: {mess[4]}\n" \
#                      f"Цена: ${mess[1]}"
#             bot.send_message(chat_id=message.chat.id, text=answer,
#                              parse_mode="html",
#                              reply_markup=hotel_website(hotel_name=mess[0],
#                                                         hotel_id=mess[2],
#                                                         check_in=check_in,
#                                                         check_out=check_out))
#
#     bot.register_next_step_handler(message=message,
#                                    callback=end(message=message))
#     bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
#
#
# def end(message: types.Message) -> None:
#     # здесь будет добавлен код по записи в БД
#     bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
#     answer = "Это все, что я могу предложить по вашему запросу"
#     bot.send_message(chat_id=message.chat.id, text=answer, parse_mode="html",
#                      reply_markup=user_keyboard())
