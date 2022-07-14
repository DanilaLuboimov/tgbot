from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    user_id = State()
    user_filter = State()
    city_name = State()
    city_id = State()
    check_in = State()
    check_out = State()
    price_min = State()
    price_max = State()
    need_photos = State()
    count_photos = State()
    count_hotels = State()
    distance_min = State()
    distance_max = State()
