from loader import bot
from telebot.types import Message
from keyboards.reply.default_keyboard import user_keyboard
from utils.info import info
from utils.logging import ex_log


@bot.message_handler(commands=["help"])
@ex_log
def help_info(message: Message) -> None:
    """
    Сообщение для пользователя о возможностях бота и клавиатура с командами

    :param message: Сообщение от пользователя
    :type message: Message
    :return: None
    """
    answer = info()
    bot.send_message(message.chat.id, answer, parse_mode='html',
                     reply_markup=user_keyboard())
