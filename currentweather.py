from typing import Optional
from fastapi import Query
import aiosqlite
from classes import WeatherResponse
import json


BASE_URL = "https://api.open-meteo.com/v1/forecast"

# 4.	Метод принимает название города и время и возвращает для него погоду на текущий день в указанное время,
#       должна быть возможность выбирать какие параметры погоды получаем в ответе – температура, влажность,
#       скорость ветра, осадки.


async def get_weather_by_hour(city: str, time_w: str,
                              temperature: Optional[bool] = Query(None),
                              humidity: Optional[bool] = Query(None),
                              wind_speed: Optional[bool] = Query(None),
                              precipitation: Optional[bool] = Query(None)):
    async with aiosqlite.connect("cities.db") as db:
        async with db.execute("SELECT weather FROM cities WHERE city = ?", (city,)) as cursor:
            weather_data = await cursor.fetchone()

            if weather_data is None:
                return WeatherResponse(city=city, time_w=time_w)

            if weather_data:
                weather_json_string = weather_data[0]
                weather_json = json.loads(weather_json_string)
            else:
                weather_json = {}

            hour = time_w.split(':')[0]

            response = WeatherResponse(city=city, time_w=time_w,
                                       temperature=temperature,
                                       humidity=humidity,
                                       wind_speed=wind_speed,
                                       precipitation=precipitation)
            if temperature == True:
                response.temperature = weather_json["temperature_2m"][int(hour)-1]
            elif humidity == True:
                response.humidity = weather_json["relative_humidity_2m"][int(hour)-1]
            elif wind_speed == True:
                response.wind_speed = weather_json["wind_speed_10m"][int(hour)-1]
            elif precipitation == True:
                response.precipitation = weather_json["precipitation"][int(hour)-1]
            return response
