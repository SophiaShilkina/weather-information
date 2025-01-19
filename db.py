import aiosqlite


async def create_table_1():
    async with aiosqlite.connect('cities.db') as db:

        await db.execute('''
        CREATE TABLE IF NOT EXISTS Cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER,
        city TEXT NOT NULL,
        latitude FLOAT,
        longitude FLOAT,
        weather TEXT,
        last_updated TIMESTAMP,
        FOREIGN KEY (id_user) REFERENCES Users (id) ON DELETE CASCADE
        )
        ''')

        await db.commit()


async def create_table_2():
    async with aiosqlite.connect('users.db') as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL
        )
        ''')

        await db.commit()


async def database_implementation():
    await create_table_2()
    await create_table_1()
