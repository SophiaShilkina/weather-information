import logging
from fastapi import HTTPException
import httpx
import aiosqlite
import json
from base import async_session
from models import CitiesBase, UsersBase
from sqlalchemy import select, func, and_, update
import sqlalchemy


BASE_URL = "https://api.open-meteo.com/v1/forecast"

# 2.	Метод принимает название города и его координаты и добавляет в список городов для которых отслеживается
#       прогноз погоды - сервер должен хранить прогноз погоды для указанных городов на текущий день и
#       обновлять его каждые 15 минут.


async def fetch_column_data():
    async with aiosqlite.connect('../cities.db') as db:
        async with db.execute("SELECT city FROM cities") as cursor:
            rows = await cursor.fetchall()

            if not rows:
                logging.info("No cities found.")
                return

            for row in rows:
                logging.info(f"Information has been updated for the city {row[0]}.")
                yield row[0]


async def get_weather_city(city: str) -> None:
    async with async_session() as session:
        try:
            result = await session.execute(select(CitiesBase).where(CitiesBase.city == city))
            cities = result.scalars().all()

            coordinates = []

            for cit in cities:
                coordinates.append((cit.latitude, cit.longitude))

            latitude, longitude = coordinates[0]

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
                    raise HTTPException(status_code=response.status_code, detail="Данные о погоде недоступны.")

                data = response.json()

                daily_data = {}
                for param in hourly_params:
                    daily_data[param] = data['hourly'][param][:24] if 'hourly' in data and param in data['hourly'] else []

                daily_data = json.dumps(daily_data)

                async with session.begin():
                    stmt = update(CitiesBase).where(CitiesBase.city == city).values(weather=daily_data)
                    await session.execute(stmt)

        except Exception as e:
            logging.error(f"Error occurred: {e}")


async def generator() -> None:
    async for city in fetch_column_data():
        await get_weather_city(city)


async def add_city(usid: int, city: str, latitude: float, longitude: float) -> None:
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
                return

            user_id, city_count = user_data

            if city_count > 0:
                logging.info(f"For the user {user_id}, the city '{city}' already exists in the database.")
                return

            session.add_all(
                [
                    CitiesBase(user_id=usid, city=city, latitude=latitude, longitude=longitude),
                ]
            )
            await session.commit()

            await get_weather_city(city)

            logging.info(f"{city} added to the database for user: {usid}.")

        except sqlalchemy.exc.IntegrityError as e:
            logging.error(f"IntegrityError occurred: {e}")
