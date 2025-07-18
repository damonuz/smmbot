from aiogram import types
from aiogram.dispatcher import FSMContext
from config import ADMIN_ID
from database import register_user, balances, referrals, add_order
from check_subs import check_user_subscription
from services import services
from states import OrderState

async def handle_start(message, bot):
    user_id = message.from_user.id
    args = message.get_args()
    ref_id = int(args) if args.isdigit() else None
    await check_and_register(message, bot, user_id, ref_id)

async def check_and_register(message, bot, user_id, ref_id):
    if not await check_user_subscription(bot, user_id):
        text = "🔐 Botdan foydalanish uchun quyidagi kanallarga a’zo bo‘ling:\n\n"
        for channel in ['kanal1', 'kanal2']:
            text += f"👉 <a href='https://t.me/{channel}'>@{channel}</a>\n"
        text += "\n✅ A’zo bo‘lganingizdan so‘ng /start ni qaytadan yuboring."
        await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)
        return
    register_user(user_id, ref_id)
    await message.answer("👋 Xush kelibsiz! Pastdagi menyudan tanlang.")

async def handle_balance(message):
    user_id = message.from_user.id
    bal = balances[user_id]
    await message.answer(f"💰 Sizning balansingiz: {bal} so'm")

async def handle_referrals(message):
    user_id = message.from_user.id
    link = f"https://t.me/{(await message.bot.get_me()).username}?start={user_id}"
    count = len(referrals[user_id])
    await message.answer(f"🔗 Referal havolangiz: {link}\n👥 Taklif qilinganlar soni: {count}")

async def handle_payment(message):
    await message.answer("""💳 Iltimos, ushbu karta raqamiga tolovni amalga oshiring:

💳 4073 4200 2180 3105

🧾 So'ngra to‘lov chekini adminga yuboring: @axi5757""")

async def handle_services(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in services:
        kb.add(category)
    await message.answer("🗂 Bo‘limni tanlang:", reply_markup=kb)
    await OrderState.ChoosingCategory.set()

async def choose_category(message: types.Message, state: FSMContext):
    category = message.text
    if category not in services:
        return await message.answer("❗ Noto‘g‘ri tanlov. Qaytadan urinib ko‘ring.")
    await state.update_data(category=category)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for s in services[category]:
        kb.add(s)
    await message.answer("🔘 Xizmatni tanlang:", reply_markup=kb)
    await OrderState.ChoosingService.set()

async def choose_service(message: types.Message, state: FSMContext):
    service = message.text
    await state.update_data(service=service)
    await message.answer("🔗 Havolani yuboring:")
    await OrderState.EnteringLink.set()

async def enter_link(message: types.Message, state: FSMContext):
    link = message.text
    await state.update_data(link=link)
    await message.answer("🔢 Miqdorni kiriting (masalan: 100):")
    await OrderState.EnteringQuantity.set()

async def enter_quantity(message: types.Message, state: FSMContext):
    quantity = message.text
    data = await state.get_data()
    add_order(message.from_user.id, data['category'], data['service'], data['link'], quantity)
    await message.answer("✅ Buyurtma qabul qilindi! Narxi: 8000 so‘m")
    await state.finish()
