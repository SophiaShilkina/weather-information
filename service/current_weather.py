from typing import Optional
from fastapi import Query
import logging
from base import async_session
from sqlalchemy import select
from models import CitiesBase
from fastapi import HTTPException


# 4.	Метод принимает название города и время и возвращает для него погоду на текущий день в указанное время,
#       возможность выбирать какие параметры погоды получаем в ответе – температура, влажность,
#       скорость ветра, осадки.


async def get_weather_by_hour(usid: int, city: str, time_w: str,
                              temperature: Optional[bool] = Query(None),
                              humidity: Optional[bool] = Query(None),
                              wind_speed: Optional[bool] = Query(None),
                              precipitation: Optional[bool] = Query(None)) -> dict:
    async with async_session() as session:
        stmt = select(CitiesBase.weather).where(CitiesBase.user_id == usid, CitiesBase.city == city)
        result = await session.execute(stmt)

        weather_data = result.scalar_one_or_none()

        if not weather_data:
            logging.error("City not found.")
            raise HTTPException(status_code=404, detail="City not found.")

        hour = time_w.split(':')[0]

        response = {}

        if temperature:
            response["temperature"] = weather_data["temperature_2m"][int(hour)]
        if humidity:
            response["humidity"] = weather_data["relative_humidity_2m"][int(hour)]
        if wind_speed:
            response["wind_speed"] = weather_data["wind_speed_10m"][int(hour)]
        if precipitation:
            response["precipitation"] = weather_data["precipitation"][int(hour)]
        if not response:
            response["None"] = "Select the weather settings."

        return response
