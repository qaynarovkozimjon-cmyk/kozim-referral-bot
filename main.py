from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncio
import os

from database import create_db, add_user, get_referrals

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    args = message.text.split()

    referrer = None
    if len(args) > 1:
        try:
            referrer = int(args[1])
        except ValueError:
            pass

    if referrer == message.from_user.id:
        referrer = None

    await add_user(
        message.from_user.id,
        message.from_user.username,
        referrer
    )

    bot_username = (await bot.get_me()).username
    link = f"https://t.me/{bot_username}?start={message.from_user.id}"

    count = await get_referrals(message.from_user.id)

    await message.answer(
        f"🎉 Xush kelibsiz!\n\n"
        f"👥 Referallaringiz: {count}\n\n"
        f"🔗 Sizning referal havolangiz:\n{link}"
    )

async def main():
    await create_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
