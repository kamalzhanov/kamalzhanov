from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
# from config import token
# import asyncio

bot = Bot(token='7499176661:AAFY3zGzQgVbXtXUQPMjKT-B0JJI0BrfurU')
dp = Dispatcher(bot)
basicConfig(level=INFO)

start_buttons = [
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Курсы'),
    types.KeyboardButton('Адрес'),
    types.KeyboardButton('Контакты')
]

start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.reply(f"Здравствуйте, {message.from_user.full_name} !", reply_markup=start_keyboard)
    
@dp.message_handler(text='О нас')
async def about_as(message:types.Message):
    await message.reply("Geeks - это айти курсы в Оше, Кара-Балте, Бишкеке основанная в 2019г")
    
@dp.message_handler(text = 'Адрес')
async def send_andress(message:types.Message):
    await message.reply("Наш адрес: город ОШ, Мырзалы Аматова 1Б (БЦ 'Томирис')")
    await message.reply_location(40.51931846586533, 72.80297788183063)
    
@dp.message_handler(text= 'Контакты')
async def send_contact(message:types.Message):
    await message.answer(f'{message.from_user.full_name}, вот наши контакты: ')
    await message.answer_contact("+996505180600", "Islam", "Toksonbaev")
    await message.answer_contact("+996222226070", "Syimyk", "Abdykadyrov")
    
courses = [
    types.KeyboardButton("Backend"),
    types.KeyboardButton("Frontend"),
    types.KeyboardButton("Android"),
    types.KeyboardButton("IOS"),
    types.KeyboardButton("UX/UI"),
    types.KeyboardButton("Детское программирование"),
    types.KeyboardButton("Основы программирования"),
    types.KeyboardButton("Оставить заявку"),
    types.KeyboardButton("Назад")      
]

courses_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses)

@dp.message_handler(text = "Курсы")
async def all_courses(message:types.Message):
    await message.answer("Вот наши курсы: ", reply_markup=courses_keyboard)
    
@dp.message_handler(text='Backend')
async def about_as(message:types.Message):
    await message.reply("Backend - это серверная сторона сайта или приложения. В основном код вам не виден")
    
@dp.message_handler(text='Frontend')
async def about_as(message:types.Message):
    await message.reply("Frontend - это лицевая сторона сайта или приложения. Эту часть вы можете видеть")
    
@dp.message_handler(text='Android')
async def about_as(message:types.Message):
    await message.reply("Android - это разработка мобильного приложения. С ОС Android")

@dp.message_handler(text='UX/UI')
async def about_as(message:types.Message):
    await message.reply("UX/UI - это дизайн сайта или приложения.")
    
@dp.message_handler(text="Назад")
async def back_start(message:types.Message):
    await start(message)
    
@dp.message_handler(text = "Оставить заявку")
async def application(message:types.Message):
    button = types.KeyboardButton("Отправить контакт", request_contact=True)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button)
    await message.answer("Пожалуйста отправьте свой контакт", reply_markup=keyboard)
    
    
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message:types.Message):
    await message.answer(message)
    await bot.send_message(-4269502098, f"Заявка на курсы:\nИмя: {message.contact.first_name}\nФамилия: {message.contact.last_name}\nТелефон: {message.contact.phone_number}\n")
    await message.answer("Спасибо что оставили заявку!")
    await start(message)
    
executor.start_polling(dp, skip_updates=True)
