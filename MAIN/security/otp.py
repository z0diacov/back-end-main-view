import secrets
from database import redis_client
from security.config import OTP_SYMBOLS, OTP_LENGTH, OTP_EXPIRE_SECONDS

from typing import Optional
from rabbitmq import rabbitmq_client

from service import mailer
from schemas.authentication import UserDataFromToken

from database import mysql_client

class OTPClient:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        pass

    def generate_otp(self) -> str:
        return ''.join(secrets.choice(OTP_SYMBOLS) for _ in range(OTP_LENGTH))
    
    async def set_otp(self, user_id: int, sending_method: Optional[str]=None) -> str:
        otp = self.generate_otp()

        await redis_client.set(f"otp:{user_id}", otp, OTP_EXPIRE_SECONDS)

        if sending_method == 'email':
            async with mysql_client.cursor() as cursor:
                pull_by_uid = await cursor.pull(
                    "SELECT email FROM users WHERE id = %s", 
                    (user_id,)
                )
                email = pull_by_uid[0]["email"]
        
            await mailer.send_email(
                message_type='otp', 
                recipient=email, 
                data={'otp': otp}
            )

        return otp

    async def verify_otp(self, user_id: int, otp: str) -> bool:
        stored_otp = await redis_client.get(f"otp:{user_id}")

        await redis_client.delete(f"otp:{user_id}")

        if stored_otp is None:
            return False
    
        return str(stored_otp.decode()) == otp
    
otp_client = OTPClient()