from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo, model_validator 
from typing import Optional

class UserDataFromToken(BaseModel):
    uid: int
    sub: str
    family: int

class OTPData(BaseModel):
    otp: str = Field(..., json_schema_extra={"example": "111111"})