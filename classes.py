from pydantic import BaseModel, field_validator
from typing import Optional
import re
from fastapi import Query


class CityName(BaseModel):
    city: str
    latitude: float
    longitude: float


class WeatherResponse(BaseModel):
    city: str
    time_w: str
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
