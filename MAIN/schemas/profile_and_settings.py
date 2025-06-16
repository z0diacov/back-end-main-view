from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo, model_validator, HttpUrl
from typing import Optional, Any, List
from datetime import datetime
from schemas.authorization import validate_password_strength, validate_username_strength, validate_name_strength

class ChangePassword(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=64, json_schema_extra={"example": "@Strongpassword123"})
    new_password: str = Field(..., min_length=8, max_length=64, json_schema_extra={"example": "@Strongpassword123"})

    @field_validator("new_password", mode="after")
    def validate_password(cls, password: str) -> str:
        return validate_password_strength(password)
    
class UsernameOnly(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "ivan_ivanov"})

    @field_validator("username", mode="after")
    def validate_username(cls, username: str) -> str:
        return validate_username_strength(username)

class NameOnly(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50, json_schema_extra={"example": "Ivan"})

    @field_validator("name", mode="after")
    def validate_name(cls, name: Optional[str]) -> Optional[str]:
        return validate_name_strength(name)
    
class GoogleAddPassword(BaseModel):
    new_password: str = Field(..., min_length=8, max_length=64, json_schema_extra={"example": "@Strongpassword123"}),
    token: str = Field(
        ..., 
        json_schema_extra={
            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwic3ViIjoidXNlciIsImV4cCI6MTY5NTQ4MjAwMH0.uJHd1KsbK_1GykeH0p3P9m5NJ_LVPcnVP7Z7BtDHnIk"
        }
    )

    @field_validator("new_password", mode="after")
    def validate_password(cls, password: str) -> str:
        return validate_password_strength(password)
    
class HasPasswordResponse(BaseModel):
    has_password: bool

class CurrentUserProfileResponse(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "ivan_ivanov"})
    email: EmailStr = Field(..., json_schema_extra={"example": "ivan.ivanov@example.com"})
    name: Optional[str] = Field(None, min_length=2, max_length=50, json_schema_extra={"example": "Ivan"})
    profile_picture_url: str = Field(..., json_schema_extra={"example": "https://example.com/media/profile_pics/ivan.jpg"})
    is_trainer: bool
    registration_date: datetime = Field(..., json_schema_extra={"example": "2024-04-18T14:30:00Z"})

class Exercise(BaseModel):
    id: int = Field(..., ge=1)
    author_user_id: int = Field(..., ge=1)
    name: str = Field(..., max_length=100)
    description: str
    private_comments: str
    created_at: datetime
    updated_at: datetime

class Workout(BaseModel):
    id: int = Field(..., ge=1)
    author_user_id: int = Field(..., ge=1)
    name: str = Field(..., max_length=100)
    description: str
    approx_duration_minutes: int = Field(..., ge=1)
    
    picture: Optional[str] = Field(
        default=None,
        description="URL to the workout image",
        json_schema_extra={"example": "https://example.com/media/workouts/1.jpg"}
    )
    
    private_comments: str
    created_at: datetime
    updated_at: datetime

class Program(BaseModel):
    id: int = Field(..., ge=1)
    author_user_id: int = Field(..., ge=1)
    title: str = Field(..., max_length=100)
    description: str
    duration_weeks: int = Field(..., ge=1)
    cycle_number: int = Field(..., ge=1)
    
    picture: Optional[str] = Field(
        default=None,
        description="URL to the program image",
        json_schema_extra={"example": "https://example.com/media/programs/7.jpg"}
    )
    
    private_comments: str
    created_at: datetime
    updated_at: datetime

class CurrentUserTrainerProfileResponse(BaseModel):
    trainer_bio: str = Field(
        ..., 
        min_length=10,
        max_length=4000,
        json_schema_extra={"example": "Certified personal trainer with 5 years of experience in strength training and rehabilitation."}
    )
    balance: int = Field(..., ge=0, json_schema_extra={"example": 1500})
    my_exercises: Optional[List[Exercise]] = Field(default=[])
    my_workouts: Optional[List[Workout]] = Field(default=[])
    my_programs: Optional[List[Program]] = Field(default=[])

class UserProfileResponse(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "ivan_ivanov"})
    name: Optional[str] = Field(None, min_length=2, max_length=50, json_schema_extra={"example": "Ivan"})
    profile_picture_url: str = Field(..., json_schema_extra={"example": "https://example.com/media/profile_pics/ivan.jpg"})
    is_trainer: bool
    registration_date: datetime = Field(..., json_schema_extra={"example": "2024-04-18T14:30:00Z"})

class TrainerProfileResponse(BaseModel):
    trainer_bio: str = Field(
        ..., 
        min_length=10, 
        max_length=4000,
        json_schema_extra={"example": "Certified personal trainer with 5 years of experience in strength training and rehabilitation."}
    )
    trainer_exercises: Optional[List[Exercise]] = Field(default=[])
    trainer_workouts: Optional[List[Workout]] = Field(default=[])
    trainer_programs: Optional[List[Program]] = Field(default=[])

class TrainerBioOnly(BaseModel):
        trainer_bio: str = Field(
            ..., 
            min_length=10,
            max_length=4000,
            json_schema_extra={"example": "Certified personal trainer with 5 years of experience in strength training and rehabilitation."}
        )