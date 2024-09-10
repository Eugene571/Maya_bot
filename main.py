import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import logging
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('BOT_API_TOKEN')

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Список продуктов и их цены
products = {
    'Соляр': 3444,
    'Ешь, молись, люби': 2444,
    'Красотка': 2222,
    'Завтрак у Тиффани': 990,
    'Волк с Уолл-Стрит - полная версия': 2777,
    'Волк с Уолл-Стрит - краткая версия': 990,
    'Душа': 2999,
    'Магия лунного света': 2222,
    'Она': 2111,
    'Спеши любить': 2222,
    'Осень в Нью-Йорке': 1490,
    'Коридор затмений': 790
}

# Главное меню с кнопками
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
for product in products.keys():
    main_menu.add(KeyboardButton(product))


# Начало работы с ботом
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот для заказа астрологических продуктов от Нади. Выберите продукт:", reply_markup=main_menu)


# Запрос даты рождения после выбора продукта
@dp.message_handler(lambda message: message.text in products)
async def ask_birth_date(message: types.Message):
    selected_product = message.text
    price = products[selected_product]
    await message.answer(f"Вы выбрали {selected_product}. Стоимость: {price} руб.\nВведите дату вашего рождения (в формате ДД.ММ.ГГГГ):")


# Запрос времени рождения
@dp.message_handler(lambda message: message.text.count('.') == 2)
async def ask_birth_time(message: types.Message):
    await message.answer("Введите время вашего рождения (в формате ЧЧ:ММ):")


# Запрос места рождения
@dp.message_handler(lambda message: ':' in message.text)
async def ask_birth_place(message: types.Message):
    await message.answer("Введите город вашего рождения:")


# Подтверждение заказа после получения всех данных
@dp.message_handler(lambda message: message.text.isalpha())
async def confirm_order(message: types.Message):
    await message.answer("Спасибо! Ваш заказ передан Наде. Она свяжется с вами в ближайшее время.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
