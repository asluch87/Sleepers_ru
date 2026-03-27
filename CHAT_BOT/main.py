import telebot
from telebot.types import ReplyKeyboardMarkup
from database import get_db_connection
from models import Product
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('BOT_TOKEN', 'BOT_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('📦 Товары','📞 Контакты')
       
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в Магазин B2B Тапочки!\n\n"
        "Выберите действие из меню ниже:",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda message: message.text == '📦 Товары')
def show_products(message):
    """Показать список товаров"""
    session = get_db_connection()
    try:
        products = session.query(Product).filter(
            Product.is_active == True
        ).order_by(Product.name).all()
        
        if not products:
            bot.send_message(message.chat.id, "😔 Товаров пока нет в наличии")
            return
        
        # Отправляем сообщение с товарами
        for product in products:
            status = " В наличии" if product.stock_quantity > 0 else " Нет в наличии"
            
            product_text = (
                f"🛍️ *{product.name}*\n"
                f"💵 Цена: {product.price} руб.\n"
                f"📦 {status} ({product.stock_quantity} шт.)\n"
                f"🏭 Поставщик: {product.supplier}\n"
                f"🔗 [Подробнее на сайте](http://127.0.0.1:5000/product/{product.id})"
            )
            
            bot.send_message(message.chat.id, product_text, parse_mode='Markdown')
                
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при загрузке товаров")
        print(f"Ошибка: {e}")
    finally:
        session.close()

@bot.message_handler(func=lambda message: message.text == '📞 Контакты')
def show_contacts(message):
    """Показать контактную информацию"""
    contacts = (
        "📞 *Контактная информация*\n\n"
        "📍 *Адрес:* г. Москва, ул. Тестовая, д. 1\n"
        "📱 *Телефон:* +7 (999) 123-45-67\n"
        "✉️ *Email:* info@b2b-tapochki.ru\n"
        "🕒 *Время работы:* 9:00 - 21:00\n\n"
        "💬 *Для оптовых заказов обращайтесь по указанным контактам*"
    )
    bot.send_message(message.chat.id, contacts, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Обработчик всех остальных сообщений"""
    if message.text not in ['📦 Товары', '📞 Контакты']:
        bot.send_message(
            message.chat.id,
            "🤖 Пожалуйста, используйте кнопки меню ниже или команду /start"
        )

if __name__ == '__main__':
  
    
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f" Ошибка при запуске бота: {e}")