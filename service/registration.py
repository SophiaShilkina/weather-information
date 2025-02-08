import logging
import sqlalchemy
from sqlalchemy import select
from base import async_session
from models import UsersBase

# 5.    Метод предназначен для регистрации пользователей. Принимает имя пользователя и возвращает уникальный
#       идентификатор (ID) нового пользователя. Каждый пользователь может иметь свой личный список городов и
#       соответствующие прогнозы погоды.


async def add_user(username: str) -> dict:
    try:
        async with async_session() as session:
            async with session.begin():
                session.add_all(
                    [
                        UsersBase(username=username, bs=[]),
                    ]
                )

        logging.info(f"The user {username} has been added to the database.")

    except sqlalchemy.exc.IntegrityError:
        logging.error(f"The {username} already exists in the database.")

    finally:
        async with async_session() as session:
            stmt = select(UsersBase.id).where(UsersBase.username == username)
            result = await session.execute(stmt)

            usid = result.scalar_one_or_none()

            return {
                "id": usid
            } if usid is not None else None
