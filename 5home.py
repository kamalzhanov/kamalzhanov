from aiogram import Bot, Dispatcher, executor, types
from logging import basicConfig, INFO
from bs4 import BeautifulSoup
from config import token
import requests

bot = Bot(token=token)
dp = Dispatcher(bot)
basicConfig(level=INFO)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("Здравствуйте! Чтобы получить новости, введите команду /news")

@dp.message_handler(commands='news')
async def news(message: types.Message):
    await message.answer("Отправляю новости...")
    url = 'https://24.kg/'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    news_items = soup.find_all('div', class_='title')

       
executor.start_polling(dp, skip_updates=True)

