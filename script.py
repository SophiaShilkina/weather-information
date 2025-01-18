from fastapi import FastAPI, HTTPException, Query
from coordinates import get_weather_now
import aiosqlite
from cities import add_city, scheduler, generator
from db import database_implementation
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from datetime import datetime
import time
from classes import CityName, Coordinates
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
    return {
        "home_page": "home_page"
    }


@app.get('/coordinates')
async def weather_now(coors: Coordinates):
    try:
        latitude = coors.latitude
        longitude = coors.longitude
        return await get_weather_now(latitude, longitude)

    except HTTPException as e:
        raise e


@app.post('/cities')
async def add_cities(cit: CityName):
    try:
        city = cit.city
        latitude = cit.latitude
        longitude = cit.longitude
        return await add_city(city, latitude, longitude)

    except HTTPException as e:
        raise e


@app.get('/forecast')
async def cities_with_forecast():
    async with aiosqlite.connect("cities.db") as db:
        async with db.execute("SELECT city FROM cities") as cursor:
            city = await cursor.fetchall()

            if not city:
                print("Города не найдены.")
                return {
                    "Error": "Cities not found."
                }

            print(f"Города: {city}")
            return {
                'Cities': city
            }


@app.get('/currentweather')
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


PORT = 8000

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT)
