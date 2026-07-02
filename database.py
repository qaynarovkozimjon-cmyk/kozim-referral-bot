import aiosqlite

DB_NAME = "users.db"

async def create_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                referrer INTEGER,
                referrals INTEGER DEFAULT 0
            )
        """)
        await db.commit()

async def add_user(user_id, username, referrer=None):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT user_id FROM users WHERE user_id=?",
            (user_id,)
        )
        user = await cursor.fetchone()

        if user:
            return False

        await db.execute(
            "INSERT INTO users(user_id, username, referrer) VALUES(?,?,?)",
            (user_id, username, referrer)
        )

        if referrer:
            await db.execute(
                "UPDATE users SET referrals = referrals + 1 WHERE user_id=?",
                (referrer,)
            )

        await db.commit()
        return True

Keyin main.py ni quyidagicha o'zgartir:

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncio
import os

from database import create_db, add_user

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await add_user(
        message.from_user.id,
        message.from_user.username
    )

    bot_username = (await bot.get_me()).username

    link = f"https://t.me/{bot_username}?start={message.from_user.id}"

    await message.answer(
        f"Salom!\n\n"
        f"Sizning referal havolangiz:\n{link}"
    )

async def main():
    await create_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
