from aiogram import Bot
from config import REQUIRED_CHANNELS

async def check_user_subscription(bot: Bot, user_id: int):
    result = []
    for channel in REQUIRED_CHANNELS:
        chat_member = await bot.get_chat_member(f"@{channel}", user_id)
        if chat_member.status in ["member", "administrator", "creator"]:
            result.append(True)
        else:
            result.append(False)
    return all(result)
