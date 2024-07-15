from aiogram import Bot, Dispatcher, executor, types
from config import token 
import logging, sqlite3, time

from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters. state import State, StatesGroup

storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect('users.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
               id INT,
               first_name  VARCHAR (100),
               last_name  VARCHAR (100),
               username  VARCHAR (100),
               created VARCHAR (100)
);
 """)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id}")
    users_result = cursor.fetchall()
    print(users_result)
    if users_result == []:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?);",
                    (message.from_user.id, 
                     message.from_user.first_name,
                    message.from_user.last_name,  
                    message.from_user.username, time.ctime()))
        cursor.connection.commit()
    await message.answer(f'Привет {message.from_user.full_name}')

class MailingState(StatesGroup):
    text = State()

@dp.message_handler(commands='mailing')
async def mail(message:types.Message):
    await message.answer('Напишите текст для рассылки: ')
    await MailingState.text.set()

@dp.message_handler(state=MailingState.text)
async def send(message:types.Message, state:FSMContext):
    await message.answer("Начинаю рассылку...")
    cursor.execute("SELECT id FROM users;")
    user_id = cursor.fetchall()
    for user_id in user_id: 
        await bot.send_message(user_id[0], message.text)
    await message.answer('Рассылка окончена...')
executor.start_polling(dp, skip_updates=True)
