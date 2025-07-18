from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import *
from states import OrderState

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await handle_start(message, bot)

@dp.message_handler(commands=["menu"])
async def menu_cmd(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📋 Xizmatlar", "💰 Balansim", "👥 Referallarim", "➕ Balans to‘ldirish")
    await message.answer("⬇️ Pastdan menyuni tanlang:", reply_markup=kb)

@dp.message_handler(lambda m: m.text == "💰 Balansim")
async def balance_cmd(message: types.Message):
    await handle_balance(message)

@dp.message_handler(lambda m: m.text == "👥 Referallarim")
async def ref_cmd(message: types.Message):
    await handle_referrals(message)

@dp.message_handler(lambda m: m.text == "➕ Balans to‘ldirish")
async def pay_cmd(message: types.Message):
    await handle_payment(message)

@dp.message_handler(lambda m: m.text == "📋 Xizmatlar")
async def services_cmd(message: types.Message, state: FSMContext):
    await handle_services(message, state)

@dp.message_handler(state=OrderState.ChoosingCategory)
async def category_handler(message: types.Message, state: FSMContext):
    await choose_category(message, state)

@dp.message_handler(state=OrderState.ChoosingService)
async def service_handler(message: types.Message, state: FSMContext):
    await choose_service(message, state)

@dp.message_handler(state=OrderState.EnteringLink)
async def link_handler(message: types.Message, state: FSMContext):
    await enter_link(message, state)

@dp.message_handler(state=OrderState.EnteringQuantity)
async def quantity_handler(message: types.Message, state: FSMContext):
    await enter_quantity(message, state)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
