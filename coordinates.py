from fastapi import HTTPException
import httpx
from datetime import datetime

BASE_URL = "https://api.open-meteo.com/v1/forecast"


async def get_weather_now(latitude: float, longitude: float):
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

