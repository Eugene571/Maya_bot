import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
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

# Хранение состояния пользователя
user_state = {}

# Обработчик команды /start
@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Привет! Я бот для заказа астрологических продуктов от Нади. Выберите продукт:", reply_markup=main_menu)
    user_state[message.from_user.id] = {'step': 'product'}

# Кастомные фильтры для обработки сообщений
def is_product_choice(message: types.Message):
    return message.text in products.keys()

def is_date_format(text: str):
    return '.' in text and text.count('.') == 2

def is_time_format(text: str):
    return ':' in text

def is_city_name(text: str):
    return text.isalpha()

# Обработчик выбора продукта
@dp.message(lambda message: is_product_choice(message))
async def ask_birth_date(message: types.Message):
    user_id = message.from_user.id
    selected_product = message.text
    price = products[selected_product]
    await message.answer(f"Вы выбрали {selected_product}. Стоимость: {price} руб.\nВведите дату вашего рождения (в формате ДД.ММ.ГГГГ):")
    user_state[user_id] = {'step': 'birth_date', 'product': selected_product}

# Запрос даты рождения
@dp.message(lambda message: is_date_format(message.text))
async def ask_birth_time(message: types.Message):
    user_id = message.from_user.id
    if is_date_format(message.text):
        await message.answer("Введите время вашего рождения (в формате ЧЧ:ММ):")
        user_state[user_id]['step'] = 'birth_time'
    else:
        await message.answer("Введите дату в правильном формате (ДД.ММ.ГГГГ).")

# Запрос времени рождения
@dp.message(lambda message: is_time_format(message.text))
async def ask_birth_place(message: types.Message):
    user_id = message.from_user.id
    if is_time_format(message.text):
        await message.answer("Введите город вашего рождения:")
        user_state[user_id]['step'] = 'birth_place'
    else:
        await message.answer("Введите время в правильном формате (ЧЧ:ММ).")

# Запрос места рождения
@dp.message(lambda message: is_city_name(message.text))
async def confirm_order(message: types.Message):
    user_id = message.from_user.id
    if is_city_name(message.text):
        # Отправка подтверждения пользователю
        await message.answer("Спасибо! Ваш заказ передан Наде. Она свяжется с вами в ближайшее время.")
        
        # Формирование сообщения с деталями заказа
        user_info = user_state.get(user_id, {})
        product = user_info.get('product', 'Неизвестен')
        birth_date = user_info.get('birth_date', 'Не указана')
        birth_time = user_info.get('birth_time', 'Не указано')
        birth_place = user_info.get('birth_place', 'Не указан')
        
        order_message = (
            f"Новый заказ от пользователя @{message.from_user.username}:\n"
            f"Продукт: {product}\n"
            f"Дата рождения: {birth_date}\n"
            f"Время рождения: {birth_time}\n"
            f"Место рождения: {birth_place}\n"
        )
        
        # Отправка сообщения в чат с Надей
        await bot.send_message(NADIAMAEVSKAYA_CHAT_ID, order_message)
        
        # Очистка состояния пользователя после завершения
        user_state.pop(user_id, None)
    else:
        await message.answer("Введите город в правильном формате.")

async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запуск главной функции через event loop
    asyncio.run(main())
