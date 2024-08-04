from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from config import token
import requests, time, aioschedule, asyncio, logging


bot = Bot(token=token)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

monitoring = False
chat_id = None

async def get_btc_price():
    url = 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    response = requests.get(url=url).json()
    price = response.get('price')
    if price:
        return f'Стоимость биткоина на {time.ctime()}, {price}'
    else:
        return f'Не удалось получить цену биткоина'
    
async def schedule():
    global monitoring 
    while monitoring:
        message = await get_btc_price()
        await bot.send_message(chat_id, message)
        await asyncio.sleep(1)
        
@dp.message(Command('start'))
async def start(message:Message):
    await message.answer(f'Привет {message.from_user.full_name}')
    
@dp.message(Command('help'))
async def help(message:Message):
    await message.answer('Я бот для мониторинга цены биткоина. Используй команду /btc для начала мониторинга и /stop для его остановки.')
    
@dp.message(Command("btc"))
async def btc(message:Message):
    global chat_id, monitoring
    chat_id = message.chat.id
    monitoring = True
    await message.answer("Начало мониторинга цены.")
    await schedule()
    
@dp.message(Command('stop'))
async def stop(message:Message):
    global monitoring
    monitoring = False
    await message.answer("Мониторинг цены остановлен")
    
async def on_startup():
    await bot.set_my_commands([
        BotCommand(command="/start", description= 'Start bot'),
        BotCommand(command="/help", description= 'Help'),
        BotCommand(command="/btc", description= 'Start BTC monitoring'),
        BotCommand(command="/stop", description= 'Stop BTC monitoring')
    ])
    logging.info("Бот запущен и готов к работе")
    
async def main():
    dp.startup.register(on_startup)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())