from pydantic import BaseModel, field_validator, Field
from typing import Optional
import re
from fastapi import Query


class Coordinates(BaseModel):
    latitude: float = Field(..., description="Широта должна быть в диапазоне от -90 до 90.")
    longitude: float = Field(..., description="Долгота должна быть в диапазоне от -180 до 180.")

    @field_validator("latitude")
    def latitude_range(cls, value):
        if not -90 <= value <= 90:
            raise ValueError("Широта должна быть в диапазоне от -90 до 90.")
        return value

    @field_validator("longitude")
    def longitude_range(cls, value):
        if not -180 <= value <= 180:
            raise ValueError("Долгота должна быть в диапазоне от -180 до 180.")
        return value


class CityName(BaseModel):
    city: str
    latitude: float
    longitude: float


class WeatherResponse(BaseModel):
    city: str
    time_w: str = Field(..., description="Неверный формат времени или временной диапазон.")
    temperature: Optional[bool] = Query(None)
    humidity: Optional[bool] = Query(None)
    wind_speed: Optional[bool] = Query(None)
    precipitation: Optional[bool] = Query(None)

    @field_validator("time_w")
    def ensure_time_format(cls, v):

        if not re.match(r'^\d{2}:\d{2}$', v):
            raise ValueError("Нужен формат времени HH:MM.")

        hours, minutes = map(int, v.split(':'))
        if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
            raise ValueError("Часы должны быть между 0 и 23, минуты между 0 и 59.")
        return v
