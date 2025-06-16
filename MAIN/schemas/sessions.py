from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo, model_validator 
from datetime import datetime

class Session(BaseModel):
    session_id: int
    ip: str
    os: str | None = None
    browser: str | None = None
    device: str | None = None
    location_country:  str | None = None
    location_region: str | None = None
    location_city: str | None = None
    location_lat: float | None = None
    location_lon: float | None = None
    location_isp: str | None = None
    login_at: datetime

class MyActiveSessionsResponse(BaseModel):
    sessions: list[Session]