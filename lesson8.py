from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import LabeledPrice, PreCheckoutQuery, CallbackQuery, Message, BotCommand
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio, logging
from config import token

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

logging.basicConfig(level=logging.INFO)

@router.message(Command("start"))
async def start(message:Message):
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="Купить ноутбук", callback_data='buy_laptop')
        keyboard.adjust(1)
        await message.reply("Привет! Выбери товар для покупки. ", reply_markup=keyboard.as_markup())
        
@router.callback_query(lambda c: c.data == 'buy_laptop')
async def process_payment(callback_query: CallbackQuery):
    price = [LabeledPrice(label='HP Victus', amount=70000)]
    
    await bot.send_invoice(
        chat_id=callback_query.from_user.id,
        title='Ноутбук',
        payload="laptop",
        description='Ноутбук HP VICTUS 15-fa0031dx Intel Core i5-12450H(3.30-4.40GHz),8GB DDR4,512GB SSD m.2 NVMe,NVIDIA GTX 1650 4GB GDDR6,15.6" FHD(1920x1080)144Hz IPS,WiFi ac,BT 5.0,HD WC,CR,Win11,MicaSilv[68U87UA#ABA]',
        provider_token= '1744374395:TEST:9ffd9c28eabf8b18e1eb',
        currency='RUB',
        prices=price,
        start_parameter='test_bot',
        photo_url='https://www.ultra.kg/upload/resize_cache/iblock/abb/1000_1000_1d0e97ea46f4438969ab06dd5b311ca67/abb3c7028d30f6d965fa949510ad6426.jpg',
        photo_height=512,
        photo_width=512,
        photo_size=512,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        is_flexible=False 
    )
    
@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
    

@router.message(lambda message: message.ok_payments is not None)
async def ok_payments(message:Message):
    await message.reply("Спасибо за покупку!")  


async def on_startup():
    await bot.set_my_commands(
        BotCommand(command="/start", description= 'Start bot'))

async def main():
    dp.startup.register(on_startup)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())
