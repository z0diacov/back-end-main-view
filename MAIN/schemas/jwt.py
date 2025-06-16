from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo, model_validator 

class JWTAccess(BaseModel):
    type: str = "access"
    family: int
    iter: int
    uid: int
    sub: str

class JWTRefresh(BaseModel):
    type: str = "refresh"
    family: int
    iter: int
    uid: int
    sub: str

class JWTVerifyEmail(BaseModel):
    type: str = "verify_email"
    email: EmailStr
    family: int

class JWTResetPassword(BaseModel):
    type: str = "reset_password"
    email: EmailStr
    family: int

class JWTGooglePassword(BaseModel):
    type: str = "google_add_password"
    email: EmailStr
    family: int