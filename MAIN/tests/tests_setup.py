import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from security.config import SECRET_KEY, ALGORITHM
from typing import Any
from tests.database_for_tests import mysql_client_sync
from tests.database_for_tests import redis_client_sync

class TestsSetup:


    def __init__(self) -> None:
        self.connection = None

    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def create_not_decoded_jwts(self, type: str) -> dict[Any]:

        not_decoded_jwts: dict[str, dict[str, str] | None] = {
            "Invalid_email_token": {
                "email": "email_confirm_token",
                "family": 1,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            },
            "Random_type_token": {
                "email": "user@example.com",
                "family": 1,
                "type": ":)",
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            },
            "Verify_email_token": {
                "email": "user@example.com",
                "family": 1,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            },
            "Valid_token": {
                "email": "root@example.com",
                "family": 1,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            },
            "Expired_token": {
                "email": "admin@example.com",
                "family": 1,
                "type": type,
                "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
            },
            "Wrong_token": {
                "test": "dfpogkd;flkg;dflkg",
                "type": type
            },
            "Already_verified": {
                "email": "root@example.com",
                "family": 1,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            },
            "Nonexistent_token": {
                "email": "vikingragnar912@gmail.com",
                "family": 1,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            },
            "Google_registrated_no_pass_token": {
                "email": "google@example.com",
                "family": 5,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            }
        }

        mysql_client_sync.connect()

        if type == "verify_email":
            with mysql_client_sync.cursor() as cursor:
                cursor.push(f"INSERT INTO {type}_activity (user_id) VALUES (%s)", (3))
        elif type != "google_add_password":
            with mysql_client_sync.cursor() as cursor:
                cursor.push(f"INSERT INTO {type}_activity (user_id) VALUES (%s)", (1))

        mysql_client_sync.disconnect()

        return not_decoded_jwts
    
    def create_not_decoded_iter_jwts(self, type: str) -> dict[Any]:

        not_decoded_jwts: dict[str, dict[str, str] | None] = {
            "Random_type_token": {
                "uid": 1,
                "sub" : "root",
                "family": 1,
                "iter": 1,
                "type": ":)",
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
            },
            "Verify_email_token": {
                "uid": 3,
                "sub" : "user",
                "family": 1,
                "iter": 1,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
            },
            "Expired_token": {
                "uid": 1,
                "sub" : "root",
                "family": 1,
                "iter": 1,
                "type": type,
                "exp": datetime.now(timezone.utc) - timedelta(minutes=5)
            },
            "Wrong_token": {
                "test": "dfpogkd;flkg;dflkg",
                "type": type
            },
            "Nonexistent_token": {
                "uid": 7,
                "sub" : "Ragnar",
                "family": 1,
                "iter": 1,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
            },
            "Invalid_uid_token": {
                "uid": "1",
                "sub" : "Ragnar",
                "family": 1,
                "iter": 1,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
            }, 
            "Invalid_iter_token": {
                "uid": 1,
                "sub" : "root",
                "family": 3,
                "iter": 0,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
            }, 
            "Valid_token_family_3": {
                "uid": 1,
                "sub" : "root",
                "family": 3,
                "iter": 1,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
            },
            "Valid_token_family_2": {
                "uid": 2,
                "sub" : "admin",
                "family": 2,
                "iter": 1,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
            },
            "Google_registrated_no_pass_token": {
                "uid": 4,
                "sub": "google",
                "iter": 1,
                "family": 5,
                "type": type,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            }
        }

        return not_decoded_jwts
    
tests_setup = TestsSetup()