from pydantic import BaseModel, field_validator, Field
from typing import Optional
import re
from fastapi import Query


class UserName(BaseModel):
    username: str


class CityName(BaseModel):
    city: str
    latitude: float = Field(..., description="The latitude should be in the range of -90 to 90.")
    longitude: float = Field(..., description="The longitude should be in the range from -180 to 180.")

    @field_validator("latitude")
    def latitude_range(cls, value):
        if not -90 <= value <= 90:
            raise ValueError("The latitude should be in the range of -90 to 90.")
        return value

    @field_validator("longitude")
    def longitude_range(cls, value):
        if not -180 <= value <= 180:
            raise ValueError("The longitude should be in the range from -180 to 180.")
        return value


class WeatherResponse(BaseModel):
    city: str
    time_w: str = Field(..., description="Incorrect time format or time range.")
    temperature: Optional[bool] = Query(None)
    humidity: Optional[bool] = Query(None)
    wind_speed: Optional[bool] = Query(None)
    precipitation: Optional[bool] = Query(None)

    @field_validator("time_w")
    def ensure_time_format(cls, v):

        if not re.match(r'^\d{2}:\d{2}$', v):
            raise ValueError("The required time format is HH:mm.")

        hours, minutes = map(int, v.split(':'))
        if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
            raise ValueError("The hours should be between 0 and 23, the minutes between 0 and 59.")
        return v
