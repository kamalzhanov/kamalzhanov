import logging
import smtplib
import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message

token = '7499176661:AAFY3zGzQgVbXtXUQPMjKT-B0JJI0BrfurU'
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_sender = 'kamalzhanov118@gmail.com'
smtp_sender_password = "qwtt pxbd zsvv whgm"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class EmailForm(StatesGroup):
    email = State()
    subject = State()
    message = State()

def create_db():
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def saveemail(email, subject, message):
    try:
        conn = sqlite3.connect('emails.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO emails (email, subject, message)
        VALUES (?, ?, ?)
        ''', (email, subject, message))
        conn.commit()
        conn.close()
        logging.info("Данные сохранены в базу данных")
    except Exception as exe:
        logging.error(f"Ошибка при сохранении в базу данных: {exe}")

def sendemail(to_email, subject, message):
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_sender, smtp_sender_password)
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(smtp_sender, to_email, email_message)
        logging.info("Email отправлен")
    except Exception as e:
        logging.error(f"Ошибка при отправке email: {e}")

@dp.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(EmailForm.email)
    await message.reply("Привет! Введите ваш Gmail-адрес:")

@dp.message(EmailForm.email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(EmailForm.subject)
    await message.reply("Введите тему письма:")

@dp.message(EmailForm.subject)
async def process_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(EmailForm.message)
    await message.reply("Введите сообщение:")

@dp.message(EmailForm.message)
async def process_message(message: Message, state: FSMContext):
    data = await state.get_data()
    email = data['email']
    subject = data['subject']
    message_text = message.text
    
    logging.info(f"Отправка email на адрес: {email}, тема: {subject}, сообщение: {message_text}")
    saveemail(email, subject, message_text)
    sendemail(email, subject, message_text)
    
    await state.clear()
    await message.reply("Ваше сообщение было отправлено и сохранено в базе данных.")

async def on_startup(dispatcher: Dispatcher):
    logging.info("Настройки базы")
    create_db()
    logging.info("База загружена")

async def main():
    await on_startup(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

