from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def hotel_website(hotels: list) -> InlineKeyboardMarkup:
    """
    Функция создает встроенную клавиатуру с ссылками отелей

    :param hotels: Элементы (url отеля, название отеля)
    :type hotels: list
    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()

    for button in hotels:
        hotel_url = button[0]
        hotel_name = button[1]

        hotel_site = InlineKeyboardButton(text=hotel_name, url=hotel_url)

        markup.add(hotel_site)

    return markup
