from fastapi import HTTPException, Query
from service.coordinates import get_weather_now
from service.cities import add_city
from service.forecast import cities_with_forecast
from entities import CityName, UserName
from service.current_weather import get_weather_by_hour
from service.registration import add_user
from typing import Optional
from scheduler import lifespan
from fastapi import FastAPI


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def home_page() -> dict:
    return {
        "home_page": "home_page"
    }


@app.get('/coordinates')
async def weather_now(latitude: float = Query(..., ge=-90, le=90),
                      longitude: float = Query(..., ge=-180, le=180),) -> dict:
    try:
        return await get_weather_now(latitude, longitude)

    except HTTPException as e:
        raise e


@app.post('/registration')
async def add_users(us: UserName) -> dict:
    try:
        username = us.username
        return await add_user(username)

    except HTTPException as e:
        raise e


@app.post('/cities/{usid}')
async def add_cities(usid: int, cit: CityName) -> None:
    try:
        city = cit.city
        latitude = cit.latitude
        longitude = cit.longitude
        return await add_city(usid, city, latitude, longitude)

    except HTTPException as e:
        raise e


@app.get('/forecast/{usid}')
async def available_cities_for_user(usid: int) -> list:
    try:
        return await cities_with_forecast(usid)

    except HTTPException as e:
        raise e


@app.get('/currentweather/{usid}')
async def read_weather(usid: int, city: str, time_w: str,
                       temperature: Optional[bool] = Query(None),
                       humidity: Optional[bool] = Query(None),
                       wind_speed: Optional[bool] = Query(None),
                       precipitation: Optional[bool] = Query(None)) -> dict:
    try:
        return await get_weather_by_hour(usid, city, time_w,
                                         temperature,
                                         humidity,
                                         wind_speed,
                                         precipitation)

    except HTTPException as e:
        raise e
