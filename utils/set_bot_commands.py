from telebot.types import BotCommand
from config_data.config import commands


def set_commands(bot) -> None:
    """
    Функция создания меню с командами для бота

    :param bot: токен вашего бота
    :return: None
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in commands]
    )
