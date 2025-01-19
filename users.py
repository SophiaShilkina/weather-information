import aiosqlite


async def add_user(username: str):
    async with aiosqlite.connect('users.db') as db:
        try:
            await db.execute('''
                    INSERT INTO Users (username) VALUES (?)
                    ''', (username,))
            await db.commit()
            print(f"Пользователь {username} добавлен в базу данных.")

            async with db.execute('SELECT id FROM Users WHERE username = ?', (username,)) as cursor:
                usid = await cursor.fetchone()
                return {
                    "id": usid
                }

        except aiosqlite.IntegrityError:
            print(f"Пользователь {username} уже существует в базе данных.")

            async with db.execute('SELECT id FROM Users WHERE username = ?', (username,)) as cursor:
                usid = await cursor.fetchone()
                return {
                    "id": f"The {username} already exists in the database on id: {usid}."
                }
