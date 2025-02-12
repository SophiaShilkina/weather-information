import logging
from base import async_session
from sqlalchemy import select
from models import CitiesBase
from fastapi import HTTPException


# 3.    Метод возвращает список городов, для которых доступен прогноз погоды для определенного пользователя.


async def cities_with_forecast(usid: int) -> list:
    async with async_session() as session:
        stmt = select(CitiesBase.city).where(CitiesBase.user_id == usid)
        result = await session.execute(stmt)

        cities_list = result.scalars().all()

        if not cities_list:
            logging.info("Cities not found.")
            raise HTTPException(status_code=404, detail="Cities not found.")

        logging.info(f"Cities: {cities_list}.")
        return cities_list
