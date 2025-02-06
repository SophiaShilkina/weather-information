import aiosqlite
import logging

# 3.    Метод возвращает список городов, для которых доступен прогноз погоды для определенного пользователя.


async def cities_with_forecast(usid: int):
    async with aiosqlite.connect("../cities.db") as db:
        async with db.execute("SELECT city FROM cities WHERE id_user = ?", (usid,)) as cursor:
            cities_tpl = await cursor.fetchall()

            if not cities_tpl:
                logging.info("Cities not found.")
                return {
                    "Error": "Cities not found."
                }

            cities_list = [city[0] for city in cities_tpl]

            logging.info(f"Cities: {cities_list}.")
            return cities_list
