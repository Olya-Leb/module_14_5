from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

api = "7657515087:AAEHpP3k31bOpOJnVB2n5bQ2YqIKUlwdy-A"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ],
        [KeyboardButton(text='Купить')],
        [KeyboardButton(text="Регистрация")],
    ], resize_keyboard=True
)
gender_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Женский'),
            KeyboardButton(text='Мужской')
        ],
    ], resize_keyboard=True
)
calc_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
        ]
    ], resize_keyboard=True
)
buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Product1', callback_data='product_buying'),
            InlineKeyboardButton(text='Product2', callback_data='product_buying'),
            InlineKeyboardButton(text='Product3', callback_data='product_buying'),
            InlineKeyboardButton(text='Product4', callback_data='product_buying')
        ]
    ], resize_keyboard=True
)

@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=main_menu_kb)

@dp.message_handler(text="Купить")
async def get_buying_list(message):
    products = get_all_products()
    for product in products:
        await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
        with open(f"files/{product[0]}.png", "rb") as img:
            await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup=buy_kb)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text="Информация")
async def info(message):
    await message.answer("Тут будет информация")

@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=calc_kb)

@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.message.answer("для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) is False:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    if is_included(message.text) is True:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data["username"], data["email"], data["age"])
    await message.answer('Регистрация прошла успешна ')
    await state.finish()

class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text="calories")
async def set_gender(call):
    await call.message.answer('Введите свой пол:\n"Женский" или "Мужской"', reply_markup=gender_kb)
    await call.answer()
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def set_age(message, state):
    await state.update_data(gender=message.text)
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if data["gender"] == "Женский":
        formula_woman = 10 * float(data["weight"]) + 6.25 * float(data["growth"]) - 5 * float(data["age"]) - 161
        await message.answer(f'Ваша женская норма калорий в сутки равна: {formula_woman} ккал.')
        await message.answer('Рассчитано по упрощенному варианту формулы Миффлина-Сан Жеора.')
    elif data["gender"] == "Мужской":
        formula_man = 10 * float(data["weight"]) + 6.25 * float(data["growth"]) - 5 * float(data["age"]) + 5
        await message.answer(f'Ваша мужская норма калорий в сутки равна {formula_man} ккал.')
        await message.answer('Рассчитано по упрощенному варианту формулы Миффлина-Сан Жеора.')
    elif int(data["gender"]) != "Женский" or "Мужской":
        await message.answer("Вы неверно ввели свой пол!\nПожалуйста, попробуйте еще раз! 😊")
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

def main():
    executor.start_polling(dp, skip_updates=True)
if __name__ == "__main__":
    main()
