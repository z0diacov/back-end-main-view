from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo, model_validator, HttpUrl
from typing import Optional
import re

def validate_password_strength(password: str) -> str:
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"[0-9]", password):
        raise ValueError("Password must contain at least one number")
    if not re.search(r"[@$!%*?&]", password):
        raise ValueError("Password must contain at least one special character (@, $, !, %, *, ?, &)")
    return password

def validate_username_strength(username: str) -> str:
    username = username.strip()
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        raise ValueError("Username can only contain letters, numbers, and underscores")
    return username

def validate_name_strength(name: Optional[str]) -> Optional[str]:
    if name is None:
        return None
    name = name.strip()
    if not re.match(r"^[a-zA-Z\-'\s]+$", name):
        raise ValueError("Names can only contain letters, hyphens, apostrophes, and spaces")
    return name

class LoginData(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "ivan_ivanov"})
    password: str = Field(..., min_length=8, max_length=64, json_schema_extra={"example": "@Strongpassword123"})


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "ivan_ivanov"})
    email: EmailStr = Field(..., json_schema_extra={"example": "ivan.ivanov@example.com"})
    password: str = Field(..., min_length=8, max_length=64, json_schema_extra={"example": "@Strongpassword123"})
    name: Optional[str] = Field(None, min_length=2, max_length=50, json_schema_extra={"example": "Ivan"})

    @field_validator("username", mode="after")
    def validate_username(cls, username: str) -> str:
        return validate_username_strength(username)

    @field_validator("password", mode="after")
    def validate_password(cls, password: str) -> str:
        return validate_password_strength(password)

    @field_validator("name", mode="after")
    def validate_name(cls, name: Optional[str]) -> Optional[str]:
        return validate_name_strength(name)

class CreatedUserResponse(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "ivan_ivanov"})
    email: EmailStr = Field(..., json_schema_extra={"example": "ivan.ivanov@example.com"})
    name: Optional[str] = Field(None, min_length=2, max_length=50, json_schema_extra={"example": "Ivan"})

class TwoTokensResponse(BaseModel):
    access_token: str = Field(
        ..., 
        json_schema_extra={
            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwic3ViIjoidXNlciIsImV4cCI6MTY5NTQ4MjAwMH0.uJHd1KsbK_1GykeH0p3P9m5NJ_LVPcnVP7Z7BtDHnIk"
        }
    )
    refresh_token: str = Field(
        ..., 
        json_schema_extra={
            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwic3ViIjoidXNlciIsImV4cCI6MTY5NTQ4MjAwMH0.uJHd1KsbK_1GykeH0p3P9m5NJ_LVPcnVP7Z7BtDHnIk"
        }
    )
    token_type: str = Field(
        ..., 
        json_schema_extra={
            "example": "bearer"
        }
    )

class AccessTokenResponse(BaseModel):
    access_token: str = Field(
        ..., 
        json_schema_extra={
            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwic3ViIjoidXNlciIsImV4cCI6MTY5NTQ4MjAwMH0.uJHd1KsbK_1GykeH0p3P9m5NJ_LVPcnVP7Z7BtDHnIk"
        }
    )

class TokenData(BaseModel):
    username: Optional[str] = Field(
        default=None, 
        json_schema_extra={
            "example": "ivan_ivanov"
        }
    )
    id: Optional[int] = Field(
        default=None, 
        json_schema_extra={
            "example": 123
        }
    )

class Forgot_password(BaseModel):
    email: EmailStr = Field(..., json_schema_extra={"example": "ivan.ivanov@example.com"})

class Reset_password(BaseModel):
    token: str = Field(
        ..., 
        json_schema_extra={
            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwic3ViIjoidXNlciIsImV4cCI6MTY5NTQ4MjAwMH0.uJHd1KsbK_1GykeH0p3P9m5NJ_LVPcnVP7Z7BtDHnIk"
        }
    ),
    new_password: str = Field(..., min_length=8, max_length=64, json_schema_extra={"example": "@Strongpassword123"})

    @field_validator("new_password", mode="after")
    def validate_password(cls, password: str) -> str:
        return validate_password_strength(password)

class EmailOnly(BaseModel):
    email: EmailStr = Field(..., json_schema_extra={"example": "ivan.ivanov@example.com"})

class GoogleCreatedUserData(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "ivan_ivanov"})
    email: EmailStr = Field(..., json_schema_extra={"example": "ivan.ivanov@example.com"})
    name: Optional[str] = Field(None, min_length=2, max_length=50, json_schema_extra={"example": "Ivan"})

    @field_validator("name", mode="after")
    def validate_name(cls, name: Optional[str]) -> Optional[str]:
        if name is None:
            return None
        name = name.strip()
        if not re.match(r"^[a-zA-Z\-'\s]+$", name):
            raise ValueError("Names can only contain letters, hyphens, apostrophes, and spaces")
        return name

class UrlResponse(BaseModel):
    url: HttpUrl

class GoogleCreatedUserResponse(BaseModel):
    user_data: GoogleCreatedUserData
    tokens: TwoTokensResponse

class FromGoogleUserData(BaseModel):
    email: EmailStr
    name: str

class GoogleCallbackData(BaseModel):
    code: str