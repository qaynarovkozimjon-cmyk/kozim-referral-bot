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
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        )
        user = await cursor.fetchone()

        if user:
            return False

        if referrer == user_id:
            referrer = None

        if referrer:
            cursor = await db.execute(
                "SELECT * FROM users WHERE user_id=?",
                (referrer,)
            )
            ref_user = await cursor.fetchone()

            if not ref_user:
                referrer = None

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


async def get_referrals(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT referrals FROM users WHERE user_id=?",
            (user_id,)
        )
        row = await cursor.fetchone()

        if row:
            return row[0]

        return 0


async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        )
        return await cursor.fetchone()
