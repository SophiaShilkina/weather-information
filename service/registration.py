import logging

import aiosqlite

# 5.    Метод предназначен для регистрации пользователей. Принимает имя пользователя и возвращает уникальный
#       идентификатор (ID) нового пользователя. Каждый пользователь может иметь свой личный список городов и
#       соответствующие прогнозы погоды.


async def add_user(username: str) -> dict:
    async with aiosqlite.connect('../users.db') as db:
        try:
            await db.execute('''
                    INSERT INTO Users (username) VALUES (?)
                    ''', (username,))
            await db.commit()
            logging.info(f"Пользователь {username} добавлен в базу данных.")

            async with db.execute('SELECT id FROM Users WHERE username = ?', (username,)) as cursor:
                usid = await cursor.fetchone()
                return {
                    "id": usid[0]
                }

        except aiosqlite.IntegrityError:
            logging.info(f"Пользователь {username} уже существует в базе данных.")

            async with db.execute('SELECT id FROM Users WHERE username = ?', (username,)) as cursor:
                usid = await cursor.fetchone()
                return {
                    "id": f"The {username} already exists in the database on id: {usid}."
                }
