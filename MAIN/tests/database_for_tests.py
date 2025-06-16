import pymysql
import redis
from typing import Any, Optional
from contextlib import contextmanager

from security.config import SQL_CONFIG
from security.config import REDIS_CONFIG
from security.hash import hash_password

class CursorWrapperSync:
    def __init__(self, cursor: pymysql.cursors.Cursor) -> None:
        self.cursor = cursor

    def pull(self, query: str, params: tuple = ()) -> list[dict[Any]]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def push(self, query: str, params: tuple = ()) -> dict[Any]:
        self.cursor.execute(query, params)
        return {
            "rowcount": self.cursor.rowcount,
            "rownumber": self.cursor.rownumber,
            "arraysize": self.cursor.arraysize,
            "lastrowid": self.cursor.lastrowid
        }
    
    def get_last_id_from_table(self, table_name: str) -> int:
        result = self.pull(f'SELECT MAX(id) FROM {table_name}')
        return int(result[0]['MAX(id)']) if result and result[0]['MAX(id)'] is not None else 0

    def __getattr__(self, name):
        return getattr(self.cursor, name)

class CursorContextManagerSync:

    def __init__(self, connection: pymysql.Connection) -> None:
        self.connection = connection

    def __enter__(self) -> CursorWrapperSync:
        self.cursor = self.connection.cursor()
        return CursorWrapperSync(self.cursor)
    
    def __exit__(self, *args) -> None:
        self.cursor.close()
        self.connection.commit()

class MysqlClientSync:

    
    def __init__(self) -> None:
        self.connection = None

    def connect(self) -> None:
        self.connection = pymysql.connect(
            host=SQL_CONFIG["host"],
            user=SQL_CONFIG["user"],
            password=SQL_CONFIG["password"],
            database=SQL_CONFIG["db"],
            cursorclass=pymysql.cursors.DictCursor
        )

    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()

    def cursor(self):
        if self.connection is None:
            raise RuntimeError("Database connection is not established. Call connect() first.")
        
        return CursorContextManagerSync(self.connection)

    def refresh_db(self) -> None:
        try:
            with self.cursor() as cursor:
                cursor.push("SET FOREIGN_KEY_CHECKS = 0;")
                cursor.push("SHOW TABLES;")
                tables = cursor.pull("SHOW TABLES;")

                for table in tables:
                    table_name = table[f"Tables_in_{SQL_CONFIG['db']}"]
                    cursor.push(f"TRUNCATE TABLE `{table_name}`;")

                cursor.push("SET FOREIGN_KEY_CHECKS = 1;")

                test_data = [
                    ("root", "root@example.com", "Root", 1, hash_password("@Rootpassword123")),
                    ("admin", "admin@example.com", "Admin", 1, hash_password("@Adminpassword123")),
                    ("user", "user@example.com", "Test", 0, hash_password("@Userpassword123")),
                    ("google", "google@example.com", "Google", 1, None)
                ]

                for username, email, name, email_verified, password in test_data:
                    cursor.push("""
                        INSERT INTO users (username, email, name, email_verified, password)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (username, email, name, email_verified, password))

                cursor.push("INSERT INTO login_activity (user_id, login_status, logout_at, logout_status) VALUES (%s, %s, NOW(), %s)", (1, "classic", "self"))
                cursor.push("INSERT INTO login_activity (user_id, login_status) VALUES (%s, %s)", (1, "classic",))
                cursor.push("INSERT INTO login_activity (user_id, login_status) VALUES (%s, %s)", (1, "classic",))
                cursor.push("INSERT INTO login_activity (user_id, login_status) VALUES (%s, %s)", (2, "classic",))
                cursor.push("INSERT INTO login_activity (user_id, login_status) VALUES (%s, %s)", (4, "google",))

                cursor.push("INSERT INTO trainer_profiles (user_id, bio, balance) VALUES (%s, %s, %s)", 
                            (1, "Certified personal trainer with 5 years of experience in strength training and rehabilitation.", 10))

        except Exception as e:
            self.connection.rollback()



mysql_client_sync = MysqlClientSync()

class RedisClientSync:

    
    def __init__(self):
        self.redis = None

    def connect(self):
        if self.redis is None:
            self.redis = redis.Redis.from_url(REDIS_CONFIG['redis_url'],
                socket_timeout=10,
                socket_connect_timeout=10)

    def disconnect(self):
        if self.redis:
            self.redis.close()
            self.redis = None

    def set(self, key: str, value: str, expire: Optional[int] = None):
        if expire:
            self.redis.setex(key, expire, value)
        else:
            self.redis.set(key, value)

    def get(self, key: str) -> Optional[str]:
        value = self.redis.get(key)
        return value.decode('utf-8') if value else None

    def delete(self, key: str):
        self.redis.delete(key)

    def exists(self, key: str) -> bool:
        return self.redis.exists(key) > 0

    def keys(self, pattern: str = "*"):
        return self.redis.keys(pattern)
    
    def clear(self):
        if self.redis:
            self.redis.flushdb()


redis_client_sync = RedisClientSync()
