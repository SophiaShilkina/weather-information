from fastapi import HTTPException
import httpx
from datetime import datetime


BASE_URL = "https://api.open-meteo.com/v1/forecast"

# 1.    Метод принимает координаты и возвращает данные о температуре, скорости ветра и атмосферном
#       давлении на момент запроса.


async def get_weather_now(latitude: float, longitude: float):

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "pressure_msl",
        "timezone": "Europe/Moscow"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Weather data is not available.")

        data = response.json()

        hourly_data = data.get("hourly", {})
        pressure_list = hourly_data.get("pressure_msl", [])

        now = datetime.now()
        current_hour = now.hour

        current_pressure = pressure_list[current_hour] if pressure_list else None

        current_weather = data.get("current_weather", {})

        temperature = current_weather.get("temperature")
        wind_speed = current_weather.get("windspeed")

    return {
        "Temperature": temperature,
        "Wind speed": wind_speed,
        "Pressure": current_pressure
    }
