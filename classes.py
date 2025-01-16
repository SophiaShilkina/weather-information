from pydantic import BaseModel, field_validator
from enum import Enum
from typing import Dict, Optional
import re
from fastapi import Query


class CityName(BaseModel):
    city: str
    latitude: float
    longitude: float


class WeatherParams(str, Enum):
    temperature: bool = Query(False),
    humidity: bool = Query(False),
    wind_speed: bool = Query(False),
    precipitation: bool = Query(False)


class WeatherResponse(BaseModel):
    city: str
    time: str
    temperature: bool = Query(False),
    humidity: bool = Query(False),
    wind_speed: bool = Query(False),
    precipitation: bool = Query(False)

    @field_validator("time")
    def ensure_time_format(cls, v):

        if not re.match(r'^\d{2}:\d{2}$', v):
            raise ValueError("Нужен формат времени HH:MM.")

        hours, minutes = map(int, v.split(':'))
        if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
            raise ValueError("Часы должны быть между 0 и 23, минуты между 0 и 59.")
        return v
