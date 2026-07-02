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
        f"🔗 Sizning havolangiz:\n{link}"
    )
