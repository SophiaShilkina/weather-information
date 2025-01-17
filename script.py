from fastapi import FastAPI, HTTPException, Query
from coordinates import get_weather_now
import aiosqlite
from cities import add_city, scheduler, generator
from db import database_implementation
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from datetime import datetime
import time
from classes import CityName, WeatherResponse
from currentweather import get_weather_by_hour
from typing import Optional


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database_implementation()
    scheduler.add_job(generator, IntervalTrigger(minutes=15))

    scheduler.start()
    print(f"Планировщик запущен {datetime.fromtimestamp(time.time())}.")

    yield

    scheduler.shutdown()
    print("Планировщик остановлен.")


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def home_page():
    print('Доступные URI:\n'
          '"http://127.0.0.1:8000" - начальная страница\n'
          '"http://127.0.0.1:8000/coordinates" - метод принимает координаты и возвращает данные о температуре, '
          'скорости ветра и атмосферном давлении на момент запроса\n'
          '"http://127.0.0.1:8000/cities" - метод принимает название города и его координаты и добавляет в список '
          'городов для которых отслеживается прогноз погоды\n'
          '"http://127.0.0.1:8080/forecast" - метод возвращает список городов, для которых доступен прогноз погоды\n'
          'Методы:\n'
          'PowerShell: curl.exe -X GET http://127.0.0.1:8000"\n'
          'cmd.exe: curl -X GET "http://127.0.0.1:8000"\n'
          'PowerShell: curl.exe -X POST "URI" -H "Content-Type: application/json" -d \'{json}\'\n'
          'cmd.exe: curl -X POST "URI" -H "Content-Type: application/json" -d \'{json}\'\n')
    return {
        'Доступные URI:': [
            'http://127.0.0.1:8000 - начальная страница',
            'http://127.0.0.1:8000/coordinates - метод принимает координаты и возвращает данные о температуре, '
            'скорости ветра и атмосферном давлении на момент запроса',
            'http://127.0.0.1:8000/cities - метод принимает название города и его координаты и добавляет в список '
            'городов для которых отслеживается прогноз погоды',
            'http://127.0.0.1:8080/forecast - метод возвращает список городов, для которых доступен прогноз погоды'
        ],
        'Команды:': [
            'PowerShell: curl.exe -X GET/POST "UPI"',
            'cmd.exe: curl -X GET/POST "URI"',
            'PowerShell: curl.exe -X POST "URI" -H "Content-Type: application/json" -d \'{json}\'',
            'cmd.exe: curl -X POST "URI" -H "Content-Type: application/json" -d \'{json}\''
        ]
    }


@app.get('/coordinates')
async def weather_now(latitude: float, longitude: float):
    try:
        return await get_weather_now(latitude, longitude)

    except HTTPException as e:
        raise e


@app.post('/cities')
async def add_cities(cit: CityName):
    try:
        city = cit.city
        latitude = cit.latitude
        longitude = cit.longitude
        await add_city(city, latitude, longitude)

    except HTTPException as e:
        raise e


@app.get('/forecast')
async def cities_with_forecast():
    async with aiosqlite.connect("cities.db") as db:
        async with db.execute("SELECT city FROM cities") as cursor:
            city = await cursor.fetchall()

            if not city:
                print("Города не найдены.")
                return

            print(f"Города: {city}")
            return {'Города': city}


@app.get('/currentweather', response_model=WeatherResponse)
async def read_weather(city: str, time_w: str,
                       temperature: Optional[bool] = Query(None),
                       humidity: Optional[bool] = Query(None),
                       wind_speed: Optional[bool] = Query(None),
                       precipitation: Optional[bool] = Query(None)):
    return await get_weather_by_hour(city, time_w,
                                     temperature,
                                     humidity,
                                     wind_speed,
                                     precipitation)


PORT = 8080

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT)
