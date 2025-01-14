from fastapi import FastAPI
from coordinates import get_weather_now

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


PORT = 8080

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT)
