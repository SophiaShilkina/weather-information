from fastapi import FastAPI, HTTPException
from coordinates import get_weather_now
import aiosqlite
from cities import add_city, get_weather_city, scheduler, fetch_column_data, generator
from db import database_implementation
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager

from datetime import datetime
import time



@asynccontextmanager
async def lifespan(app: FastAPI):
    await database_implementation()
    scheduler.add_job(generator, IntervalTrigger(minutes=1))

    scheduler.start()
    print(f"Планировщик запущен {datetime.fromtimestamp(time.time())}.")

    yield

    await scheduler.shutdown()
    print("Планировщик остановлен.")


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def home_page():
    print('Доступные URI:\n'
          'http://127.0.0.1:8000 - начальная страница\n'
          'http://127.0.0.1:8000/coordinates - метод принимает координаты и возвращает данные о температуре, '
          'скорости ветра и атмосферном давлении на момент запроса\n'
          'http://127.0.0.1:8000/cities - метод принимает название города и его координаты и добавляет в список '
          'городов для которых отслеживается прогноз погоды\n'
          'http://127.0.0.1:8000/cities/{city} - просмотр актуальной погоды для городов для которых отслеживается '
          'прогноз погоды')
    return {
        'Доступные URI:': [
            'http://127.0.0.1:8000 - начальная страница',
            'http://127.0.0.1:8000/coordinates - метод принимает координаты и возвращает данные о температуре, '
            'скорости ветра и атмосферном давлении на момент запроса',
            'http://127.0.0.1:8000/cities - метод принимает название города и его координаты и добавляет в список '
            'городов для которых отслеживается прогноз погоды',
            'http://127.0.0.1:8000/cities/{city} - просмотр актуальной погоды для городов для которых '
            'отслеживается прогноз погоды'
        ]
    }


@app.get('/coordinates')
async def weather_now():
    try:
        latitude = float(input("Введите широту: "))
        longitude = float(input("Введите долготу: "))
        return await get_weather_now(latitude, longitude)

    except HTTPException as e:
        raise e


@app.get('/cities')
async def add_cities():
    city = input("Введите название города: ")
    await add_city(city)


@app.get("/cities/{city}")
async def get_weather(city: str):
    city = input("Введите название города: ")
    async with aiosqlite.connect("cities.db") as db:
        async with db.execute("SELECT * FROM Cities WHERE city = ?", (city,)) as cursor:
            try:
                data = await cursor.fetchone()
                print(f"Город: {data[1]}\n"
                      f"Широта: {data[2]}\n"
                      f"Долгота: {data[3]}")

            except TypeError:
                print("Город не найден в базе данных.")
                return {f"{TypeError}. Город не найден в базе данных."}

            except aiosqlite.Error as e:
                print("Ошибка базы данных.")
                return {"error": f"Ошибка базы данных: {e}"}


PORT = 8080

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT)
