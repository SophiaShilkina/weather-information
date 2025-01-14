import sqlite3


async def database_implementation():
    db = sqlite3.connect('cities.db')
    cursor = db.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cities (
    id INTEGER PRIMARY KEY,
    city TEXT NOT NULL,
    latitude FLOAT,
    longitude FLOAT
    )
    ''')

    db.commit()
    db.close()
