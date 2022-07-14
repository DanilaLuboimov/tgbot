from telebot.types import BotCommand
from config_data.config import commands


def set_commands(bot):
    bot.set_my_commands(
        [BotCommand(*i) for i in commands]
    )
