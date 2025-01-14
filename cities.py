from fastapi import HTTPException
import httpx
from datetime import datetime
import sqlite3
from coordinates import get_weather_now
from db import database_implementation

BASE_URL = "https://api.open-meteo.com/v1/forecast"

# 2.	Метод принимает название города и его координаты и добавляет в список городов для которых отслеживается
#       прогноз погоды - сервер должен хранить прогноз погоды для указанных городов на текущий день и
#       обновлять его каждые 15 минут.


async def get_weather_cities_now(city):

    db = sqlite3.connect('cities.db')
    cursor = db.cursor()

    if city ==

    latitude = float(input("Введите широту: "))
    longitude = float(input("Введите долготу: "))
    weather = await get_weather_now(latitude, longitude)
    print(weather)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "pressure_msl"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        print(response)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Weather data not available")

        data = response.json()

        hourly_data = data.get("hourly", {})
        pressure_list = hourly_data.get("pressure_msl", [])

        now = datetime.now()
        current_hour = now.hour - 3

        current_pressure = pressure_list[current_hour] if pressure_list else None

        current_weather = data.get("current_weather", {})

        temperature = current_weather.get("temperature")
        wind_speed = current_weather.get("windspeed")

        return {
            "temperature": temperature,
            "wind_speed": wind_speed,
            "pressure": current_pressure
        }

