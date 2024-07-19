import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from bs4 import BeautifulSoup
from config import token
import requests
import asyncio
import sqlite3

logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера   
bot = Bot(token=token)
dp = Dispatcher()

# Функции для работы с базой данных SQLite
def create_table():
    connection = sqlite3.connect('news.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newsx TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

def insert_news(newsx):
    connection = sqlite3.connect('news.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO news (newsx) VALUES (?)', (newsx,))
    connection.commit()
    connection.close()

def get_all_news():
    connection = sqlite3.connect('news.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM news')
    rows = cursor.fetchall()
    connection.close()
    return rows

# Обработчики сообщений
@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.answer("Здравствуйте! Чтобы получить новости, введите команду /news")

@dp.message_handler(commands=["news"])
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
                insert_news(news_title)
                await message.answer(news_title)
        else:
            await message.answer("Не удалось найти новости.")
    else:
        await message.answer("Ошибка при получении новостей.")

async def main():
    create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
