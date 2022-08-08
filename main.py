from loader import bot
from utils.set_bot_commands import set_commands
from telebot.custom_filters import StateFilter
from database.create_tables import get_tables

import handlers


if __name__ == '__main__':
    get_tables()
    bot.add_custom_filter(StateFilter(bot))
    set_commands(bot)
    bot.infinity_polling()
