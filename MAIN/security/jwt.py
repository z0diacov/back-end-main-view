import jwt
import pydantic_core
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from schemas.jwt import JWTAccess, JWTRefresh, JWTVerifyEmail, JWTResetPassword
from datetime import datetime, timedelta, timezone
from typing import Optional
from security.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_SECONDS, ACCESS_TOKEN_EXPIRE_SECONDS
from typing import Any, Type
from pydantic_core import PydanticUndefined

class JWTHandler:
    
    def __init__(self):
        pass

    def create_token(self, data: dict[str, Any], expired_seconds: int, model: Type[BaseModel]) -> str:
        valid_data = model.model_validate(data)

        expire = datetime.now(timezone.utc) + timedelta(seconds=expired_seconds)
        payload = valid_data.model_dump()
        payload.update({"exp": expire})

        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def create_access_token(self, data: dict[Any], expired_seconds=ACCESS_TOKEN_EXPIRE_SECONDS) -> str:
        return self.create_token(data.copy(), expired_seconds, JWTAccess)


    def create_refresh_token(self, data: dict[Any], expired_seconds=REFRESH_TOKEN_EXPIRE_SECONDS) -> str:
        return self.create_token(data.copy(), expired_seconds, JWTRefresh)


    def decode_token(self, token: str, model: Type[BaseModel]) -> BaseModel:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            if "exp" not in payload or "type" not in payload:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

            for field_name, field_info in model.model_fields.items():
                default_value = field_info.default

                if default_value is not PydanticUndefined and field_name in payload:
                    if payload[field_name] != default_value:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid token"
                        )

            return model.model_validate(payload)

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")

        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        except pydantic_core.ValidationError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
    def get_token_expiry(self, token: str) -> Optional[datetime]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            exp_timestamp = payload.get("exp")

            if exp_timestamp is None:
                return None

            exp_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            return exp_time if exp_time > datetime.now(timezone.utc) else None

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError):
            return None

    def get_token_seconds_to_expiry(self, token: str) ->  Optional[int]:
        exp = self.get_token_expiry(token)

        if exp:
            return int((exp - datetime.now(timezone.utc)).total_seconds())
        else:
            return None


jwt_handler = JWTHandler()