from fastapi import FastAPI, HTTPException, Query
from coordinates import get_weather_now
import aiosqlite
from cities import add_city, scheduler, generator
from db import database_implementation
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from datetime import datetime
import time
from classes import CityName, UserName
from currentweather import get_weather_by_hour
from users import add_user
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
async def weather_now(latitude: float = Query(..., ge=-90, le=90),
                      longitude: float = Query(..., ge=-180, le=180),):
    try:
        return await get_weather_now(latitude, longitude)

    except HTTPException as e:
        raise e


@app.post('/registration')
async def add_users(us: UserName):
    try:
        username = us.username
        return await add_user(username)

    except HTTPException as e:
        raise e


@app.post('/cities/{usid}')
async def add_cities(usid: int, cit: CityName):
    try:
        city = cit.city
        latitude = cit.latitude
        longitude = cit.longitude
        return await add_city(usid, city, latitude, longitude)

    except HTTPException as e:
        raise e


@app.get('/forecast/{usid}')
async def cities_with_forecast(usid: int):
    async with aiosqlite.connect("cities.db") as db:
        async with db.execute("SELECT city FROM cities WHERE id_user = ?", (usid,)) as cursor:
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


@app.get('/currentweather/{usid}')
async def read_weather(usid: int, city: str, time_w: str,
                       temperature: Optional[bool] = Query(None),
                       humidity: Optional[bool] = Query(None),
                       wind_speed: Optional[bool] = Query(None),
                       precipitation: Optional[bool] = Query(None)):
    try:
        return await get_weather_by_hour(usid, city, time_w,
                                         temperature,
                                         humidity,
                                         wind_speed,
                                         precipitation)

    except HTTPException as e:
        raise e


PORT = 8000

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT)
