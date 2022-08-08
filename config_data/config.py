import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')
PORT = os.getenv('PORT')


# commands
commands = (
    ("lowprice", "Поиск от меньшей к большей цене"),
    ("highprice", "Поиск от большей к меньшей цене"),
    ("bestdeal", "Отели, наиболее подходящие по цене и расположению от центра"),
    ("history", "Ваша история поиска"),
    ("help", "Помощь по командам бота")
)