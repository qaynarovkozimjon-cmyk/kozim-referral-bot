import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.exceptions import TelegramBadRequest

from database import create_db, add_user, get_referrals

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@Matematika_Kozim"  # Kanal username

bot = Bot(TOKEN)
dp = Dispatcher()


async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ("member", "administrator", "creator")
    except TelegramBadRequest:
        return False


@dp.message(CommandStart())
async def start(message: Message):
    # Kanalga obunani tekshirish
    if not await check_subscription(message.from_user.id):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📢 Kanalga qo'shilish",
                        url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="✅ Tekshirish",
                        callback_data="check_sub"
                    )
                ]
            ]
        )

        await message.answer(
            "❗️Botdan foydalanish uchun avval kanalga a'zo bo'ling.",
            reply_markup=keyboard
        )
        return

    args = message.text.split()

    referrer = None

    if len(args) > 1:
        try:
            referrer = int(args[1])
        except ValueError:
            referrer = None

    if referrer == message.from_user.id:
        referrer = None

    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        referrer=referrer
    )

    bot_info = await bot.get_me()

    referral_link = (
        f"https://t.me/{bot_info.username}?start={message.from_user.id}"
    )

    referrals = await get_referrals(message.from_user.id)

    await message.answer(
        f"🎉 Xush kelibsiz!\n\n"
        f"👥 Referallaringiz: {referrals}\n\n"
        f"🔗 Sizning referal havolangiz:\n\n"
        f"{referral_link}"
    )


@dp.callback_query(F.data == "check_sub")
async def check_sub(callback: CallbackQuery):
    if await check_subscription(callback.from_user.id):
        await callback.message.edit_text(
            "✅ Obuna tasdiqlandi.\n\nEndi /start ni yuboring."
        )
    else:
        await callback.answer(
            "❌ Siz hali kanalga a'zo emassiz.",
            show_alert=True
        )


async def main():
    await create_db()
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
