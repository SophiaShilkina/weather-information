from fastapi import FastAPI
from coordinates import get_weather_now
from cities import get_weather_cities_now
from db import database_implementation

app = FastAPI()


@app.get('/')
async def home_page():
    print('Чтобы посмотреть список доступных команд введите "/commands"')


@app.get('/coordinates')
async def weather_now():
    latitude = float(input("Введите широту: "))
    longitude = float(input("Введите долготу: "))
    weather = await get_weather_now(latitude, longitude)
    print(weather)

@app.get('/cities')
async def weather_cities_now():
    await database_implementation()
    city = input("Введите название города: ")
    weather_city = await get_weather_cities_now(city)
    print(weather_city)



PORT = 8080

if __name__ == '__main__':
    database_implementation()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT)
