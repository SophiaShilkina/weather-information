from typing import List
from datetime import time
import aiosqlite
from classes import WeatherParams, WeatherResponse


BASE_URL = "https://api.open-meteo.com/v1/forecast"

# 4.	Метод принимает название города и время и возвращает для него погоду на текущий день в указанное время,
#       должна быть возможность выбирать какие параметры погоды получаем в ответе – температура, влажность,
#       скорость ветра, осадки.


async def get_weather_by_hour(city: str, time_w: str, params: List[WeatherParams]) -> WeatherResponse:
    async with aiosqlite.connect("cities.db") as db:
        async with db.execute("SELECT weather FROM cities WHERE city = ?", (city,)) as cursor:
            weather_data = await cursor.fetchone()

            if weather_data is None:
                return WeatherResponse(city=city, time=time_w, requested_params=params)
            weather_data = weather_data[0]

            hour = str(time_w).split(':')[0]

            response = WeatherResponse(city=city, time=time, requested_params=params)
            for param in params:
                if param == WeatherParams.temperature:
                    response.temperature = weather_data["temperature_2m"][int(hour)-1]
                elif param == WeatherParams.humidity:
                    response.humidity = weather_data["relative_humidity_2m"][int(hour)-1]
                elif param == WeatherParams.wind_speed:
                    response.wind_speed = weather_data["wind_speed_10m"][int(hour)-1]
                elif param == WeatherParams.precipitation:
                    response.precipitation = weather_data["precipitation"][int(hour)-1]
                return response
