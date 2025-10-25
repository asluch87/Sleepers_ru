import telebot
import os
from dotenv import load_dotenv  # 1. ИМПОРТИРОВАТЬ

# 2. ЗАГРУЗИТЬ переменные из .env файла
load_dotenv()

# Теперь можно получать переменные
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    exit("Ошибка: не задан токен бота")

# Используем токен из переменной окружения
my_bot = telebot.TeleBot(BOT_TOKEN)  # ← используем переменную, а не строку

@my_bot.message_handler(commands=['start'])
def send_message(message):
    print(message.from_user.id)
    return message.from_user.id

@my_bot.message_handler(func=lambda message: True)
def sends_messages(message):
    print(f"Пользователь {message.from_user.first_name} написал: {message.text}")
    my_bot.reply_to(message, f"Ты написал: '{message.text}'")

my_bot.polling()