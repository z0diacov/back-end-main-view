from fastapi import Security, HTTPException, status, Depends, Body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database import mysql_client, redis_client

from schemas.authentication import UserDataFromToken, OTPData
from schemas.jwt import JWTAccess
from security.jwt import jwt_handler

from security.otp import otp_client

from typing import Optional

security = HTTPBearer()

class BaseAuth:

    def __init__():
        pass
    
    @classmethod
    async def required_auth(self, credentials: HTTPAuthorizationCredentials = Security(security)) -> UserDataFromToken:
        """
        Steps:
        1. checks token (signature + exp etc) -> 401
        2. check in blacklist in cache (if not exist => user already logged out (401)), 
        3. if max iter != iter from token => logout with type strange + user must relogin (403) (strange activity)
        4. create pydantic UserDataFromToken
        5. return pydantic UserDataFromToken
        """
        access_token: str = credentials.credentials
        payload = jwt_handler.decode_token(access_token, JWTAccess)

        user_id = payload.uid
        username = payload.sub
        family = payload.family
        iter = payload.iter
        
        async with mysql_client.cursor() as cursor:
            user = await cursor.pull("SELECT * FROM users WHERE id = %s AND username = %s", (user_id, username,)) #checking id and username at the same time

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="User does not exist")

        last_iter_from_redis = await redis_client.get(f"whitelist:{family}")

        if not last_iter_from_redis:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token") #logged out already
        
        if int(last_iter_from_redis) != iter: #logout (strange activity)
            await redis_client.delete(f"whitelist:{family}")
            
            async with mysql_client.cursor() as cursor:
                await cursor.push("""UPDATE login_activity SET logout_at = NOW(), logout_status = %s
                                WHERE id = %s """, ('strange', family))

            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail="User must relogin")
        
        return UserDataFromToken(uid=payload.uid, sub=payload.sub, family=family)
    
    async def optional_auth(self, credentials: HTTPAuthorizationCredentials = Security(security)) -> Optional[UserDataFromToken]:
        """
        Steps:
        1. checks token (signature + exp etc) -> 401
        2. check in blacklist in cache (if not exist => user already logged out (401)), 
        3. if max iter != iter from token => logout with type strange + user must relogin (403) (strange activity)
        4. create pydantic UserDataFromToken
        5. return pydantic UserDataFromToken or None
        """
        if credentials is None:
            return None

        return Depends(self.required_auth(credentials))
    
    def is_auth_fork(self, user_data: UserDataFromToken | None) -> bool:
        """
        Check if user is authenticated
        Steps:
        1. check user_data (if None => return False)
        2. return True
        """
        if user_data is None:
            return False

        return True



class AuthDependences(BaseAuth):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        pass

    async def otp_auth(
        self,
        otp: OTPData,
        user_data: UserDataFromToken = Depends(BaseAuth.required_auth), 
    ) -> UserDataFromToken:
        """
        Required auth with OTP
        steps:
        1. Required auth
        2. check otp in redis (if not exist or incorrect => return 401)
        3. return None (success)
        """
        user_id = user_data.uid
        otp = otp.otp

        if not await otp_client.verify_otp(user_id, otp):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                            detail="OTP expired or invalid")
        
        return user_data

auth_dependences = AuthDependences()