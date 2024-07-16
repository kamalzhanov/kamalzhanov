import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from bs4 import BeautifulSoup
from config import token
import requests

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Здравствуйте! Чтобы получить новости, введите команду /news")

@dp.message(Command("news"))
async def news(message: Message):
    await message.answer("Отправляю новости...")
    url = 'https://24.kg/'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        news_items = soup.find_all('div', class_='title')

        if news_items:
            for item in news_items:
                news_title = item.get_text(strip=True)
                await message.answer(news_title)
        else:
            await message.answer("Не удалось найти новости.")
    else:
        await message.answer("Ошибка при получении новостей.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
