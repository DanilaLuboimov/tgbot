from telegram_bot_calendar import DetailedTelegramCalendar
from calendar import monthrange
from datetime import date, timedelta


def get_calendar(is_process=False, callback_data=None, **kwargs) -> tuple:
    """
    Функция создает новый календарь

    :param is_process: флаг
    :type is_process: bool
    :param callback_data: Данные обратного вызова
    :type callback_data: dict
    :param kwargs: именованные аргументы
    :type kwargs: dict
    :return: tuple
    """
    date_upper_limit = date.today()

    for _ in range(3):
        days_in_month = \
            monthrange(date_upper_limit.year, date_upper_limit.month)[1]
        date_upper_limit += timedelta(days=days_in_month)

    if is_process:
        result, keyboard, step = DetailedTelegramCalendar(
            current_date=kwargs.get('current_date'),
            min_date=kwargs['min_date'],
            max_date=date_upper_limit,
            locale=kwargs['locale']).process(callback_data)
        return result, keyboard, step
    else:
        calendar, step = DetailedTelegramCalendar(
            current_date=kwargs.get('current_date'),
            min_date=kwargs.get('min_date'),
            max_date=date_upper_limit,
            locale=kwargs.get('locale')).build()
        return calendar, step
