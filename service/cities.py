import logging
from fastapi import HTTPException
import httpx
from base import async_session
from models import CitiesBase, UsersBase
from sqlalchemy import select, func, and_, update, distinct
import sqlalchemy
from typing import AsyncGenerator


BASE_URL = "https://api.open-meteo.com/v1/forecast"

# 2.	Метод принимает название города и его координаты и добавляет в список городов для которых отслеживается
#       прогноз погоды - сервер должен хранить прогноз погоды для указанных городов на текущий день и
#       обновлять его каждые 15 минут.


async def get_weather_city(city: str, usid: int = None) -> None:
    async with (async_session() as session):
        try:
            stmt = select(CitiesBase.latitude, CitiesBase.longitude).where(CitiesBase.city == city)
            result = await session.execute(stmt)

            cities = result.fetchall()[0]

            latitude, longitude = cities[0], cities[1]

            hourly_params = [
                "temperature_2m",
                "relative_humidity_2m",
                "wind_speed_10m",
                "precipitation"
                ]

            params = {
                "latitude": latitude,
                "longitude": longitude,
                "hourly": hourly_params,
                "timezone": "Europe/Moscow"
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(BASE_URL, params=params)

                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail="Weather data is not available.")

                data = response.json()

                daily_data = {}
                for param in hourly_params:
                    daily_data[param] = data['hourly'][param][:24] if 'hourly' in data and param in data['hourly'] else []

                if usid is not None:
                    stmt = (update(CitiesBase)
                            .where(CitiesBase.city == city, CitiesBase.user_id == usid)
                            .values(weather=daily_data))
                    await session.execute(stmt)
                    await session.commit()

                else:
                    stmt = update(CitiesBase).where(CitiesBase.city == city).values(weather=daily_data)
                    await session.execute(stmt)
                    await session.commit()

        except Exception as e:
            logging.error(f"Error occurred: {e}")


async def fetch_column_data() -> AsyncGenerator[str, None]:
    async with async_session() as session:
        try:
            stmt = select(distinct(CitiesBase.city))
            result = await session.execute(stmt)

            cities_with_the_same_name = result.scalars().all()

            if not cities_with_the_same_name:
                logging.info("No cities found.")
                return

            for city in cities_with_the_same_name:
                logging.info(f"Information has been updated for the city {city}.")
                yield city

        except Exception as e:
            logging.error(f"Error occurred: {e}")


async def generator() -> None:
    async for city in fetch_column_data():
        await get_weather_city(city)


async def add_new_city(usid: int, city: str, latitude: float, longitude: float) -> None:
    async with async_session() as session:
        try:
            result = await session.execute(
                select(UsersBase.id, func.count(CitiesBase.id))
                .outerjoin(CitiesBase, and_(CitiesBase.user_id == UsersBase.id, CitiesBase.city == city))
                .where(UsersBase.id == usid)
                .group_by(UsersBase.id)
            )

            user_data = result.fetchone()

            if user_data is None:
                logging.info("Unregistered user.")
                raise HTTPException(status_code=404, detail="Unregistered user.")

            user_id, city_count = user_data

            if city_count > 0:
                logging.info(f"For the user {user_id}, the city '{city}' already exists in the database.")
                raise HTTPException(status_code=409,
                                    detail=f"For the user {user_id}, the city '{city}' already exists in the database.")

            session.add_all(
                [
                    CitiesBase(user_id=usid, city=city, latitude=latitude, longitude=longitude),
                ]
            )
            await session.commit()

            await get_weather_city(city, usid)
            logging.info(f"{city} added to the database for user: {usid}.")

        except sqlalchemy.exc.IntegrityError as e:
            logging.error(f"IntegrityError occurred: {e}")
            raise HTTPException(status_code=409, detail="This entry already exists.")
