from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # Обработка команды /start
    if text == '/start':
        await message.answer("Привет! Я бот для заказа астрологических продуктов от Нади. Выберите продукт:", reply_markup=main_menu)
        user_state[user_id] = {'step': 'product'}
        return

    # Обработка выбора продукта
    if user_state.get(user_id, {}).get('step') == 'product':
        if text in products.keys():
            selected_product = text
            price = products[selected_product]
            await message.answer(f"Вы выбрали {selected_product}. Стоимость: {price} руб.\nВведите дату вашего рождения (в формате ДД.ММ.ГГГГ):")
            user_state[user_id] = {'step': 'birth_date', 'product': selected_product}
        else:
            await message.answer("Пожалуйста, выберите продукт из списка.")
        return

    # Запрос даты рождения
    if user_state.get(user_id, {}).get('step') == 'birth_date':
        if '.' in text and text.count('.') == 2:
            await message.answer("Введите время вашего рождения (в формате ЧЧ:ММ):")
            user_state[user_id]['step'] = 'birth_time'
        else:
            await message.answer("Введите дату в правильном формате (ДД.ММ.ГГГГ).")
        return

    # Запрос времени рождения
    if user_state.get(user_id, {}).get('step') == 'birth_time':
        if ':' in text:
            await message.answer("Введите город вашего рождения:")
            user_state[user_id]['step'] = 'birth_place'
        else:
            await message.answer("Введите время в правильном формате (ЧЧ:ММ).")
        return

    # Запрос места рождения
    if user_state.get(user_id, {}).get('step') == 'birth_place':
        if text.isalpha():
            await message.answer("Спасибо! Ваш заказ передан Наде. Она свяжется с вами в ближайшее время.")
            user_state.pop(user_id, None)  # Очистка состояния пользователя после завершения
        else:
            await message.answer("Введите город в правильном формате.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
