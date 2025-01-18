from fastapi import HTTPException
import httpx
from datetime import datetime
import aiosqlite
import time
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler


BASE_URL = "https://api.open-meteo.com/v1/forecast"

# 2.	Метод принимает название города и его координаты и добавляет в список городов для которых отслеживается
#       прогноз погоды - сервер должен хранить прогноз погоды для указанных городов на текущий день и
#       обновлять его каждые 15 минут.


scheduler = AsyncIOScheduler()


async def fetch_column_data():
    async with aiosqlite.connect('cities.db') as db:
        async with db.execute("SELECT city FROM cities") as cursor:
            rows = await cursor.fetchall()

            if not rows:
                print("Города не найдены.")
                return

            for row in rows:
                print(f"Информация обновлена для города {row[0]}.")
                yield row[0]


async def get_weather_city(city: str):
    async with aiosqlite.connect('cities.db') as db:
        async with db.execute("SELECT * FROM cities WHERE city = ?", (city,)) as cursor:
            row = await cursor.fetchone()
            latitude = row[2]
            longitude = row[3]

    hourly_params = [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m",
        "precipitation"
        ]

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": hourly_params,
        "timezone": "Europe/Moscow"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        print(response)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Данные о погоде недоступны.")

        data = response.json()

        daily_data = {}
        for param in hourly_params:
            daily_data[param] = data['hourly'][param][:24] if 'hourly' in data and param in data['hourly'] else []

        daily_data = json.dumps(daily_data)

        async with aiosqlite.connect('cities.db') as db:
            await db.execute("UPDATE cities SET weather = ? WHERE city = ?", (daily_data, city))
            await db.execute("UPDATE cities SET last_updated = ? WHERE city = ?",
                             (datetime.fromtimestamp(time.time()), city))
            await db.commit()


async def generator():
    async for city in fetch_column_data():
        await get_weather_city(city)


async def add_city(city: str, latitude: float, longitude: float):
    async with aiosqlite.connect('cities.db') as db:
        try:
            await db.execute('''
                    INSERT INTO cities (city, latitude, longitude, weather, last_updated) VALUES (?, ?, ?, ?, ?)
                    ''', (city, latitude, longitude, '-', datetime.fromtimestamp(time.time()),))
            await db.commit()
            await get_weather_city(city)

            print(f"Город {city} добавлен в базу данных.")
            return {
                "city": city,
                "add": f"{city} added to the database."
            }

        except aiosqlite.IntegrityError:
            print(f"Город {city} уже существует в базе данных.")
            return {
                "city": city,
                "add": f"The {city} already exists in the database."
            }
