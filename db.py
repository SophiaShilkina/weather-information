import aiosqlite


async def database_implementation():
    async with aiosqlite.connect('cities.db') as db:

        await db.execute('''
        CREATE TABLE IF NOT EXISTS Cities (
        id INTEGER PRIMARY KEY,
        city TEXT UNIQUE NOT NULL,
        latitude FLOAT,
        longitude FLOAT,
        weather TEXT,
        last_updated TIMESTAMP
        )
        ''')

        await db.commit()
