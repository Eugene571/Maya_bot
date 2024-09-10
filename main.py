from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, Text
import logging
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('BOT_API_TOKEN')

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

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
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=product)] for product in products.keys()
    ],
    resize_keyboard=True
)

# Начало работы с ботом
@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Привет! Я бот для заказа астрологических продуктов от Нади. Выберите продукт:", reply_markup=main_menu)

# Запрос даты рождения после выбора продукта
@dp.message(Text(contains=products.keys()))
async def ask_birth_date(message: types.Message):
    selected_product = message.text
    price = products[selected_product]
    await message.answer(f"Вы выбрали {selected_product}. Стоимость: {price} руб.\nВведите дату вашего рождения (в формате ДД.ММ.ГГГГ):")

# Запрос времени рождения
@dp.message(Text(contains='.'))
async def ask_birth_time(message: types.Message):
    if message.text.count('.') == 2:
        await message.answer("Введите время вашего рождения (в формате ЧЧ:ММ):")

# Запрос места рождения
@dp.message(Text(contains=':'))
async def ask_birth_place(message: types.Message):
    if ':' in message.text:
        await message.answer("Введите город вашего рождения:")

# Подтверждение заказа после получения всех данных
@dp.message(Text(contains=''))  # Можно изменить условие в зависимости от вашего логического условия
async def confirm_order(message: types.Message):
    if message.text.isalpha():
        await message.answer("Спасибо! Ваш заказ передан Наде. Она свяжется с вами в ближайшее время.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
