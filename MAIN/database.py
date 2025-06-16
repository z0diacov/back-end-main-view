import asyncio
import aiomysql
import aiobotocore

from typing import Any, AsyncIterator, Optional, Callable,  Awaitable, Union, BinaryIO
from contextlib import asynccontextmanager
import redis.asyncio as redis

import inspect

from security.config import SQL_CONFIG
from security.config import REDIS_CONFIG
from security.config import S3_CONFIG


ExpireCallback = Callable[[str], Union[Awaitable[None], None]]

class CursorWrapper:


    def __init__(self, cursor: aiomysql.Cursor) -> None:
        self.cursor = cursor

    async def pull(self, query: str, params: tuple = ()) -> list[dict[Any]]:
        await self.cursor.execute(query, params)
        return await self.cursor.fetchall()

    async def push(self, query: str, params: tuple = ()) -> dict[Any]:
        await self.cursor.execute(query, params)
        return {
            "rowcount": self.cursor.rowcount,
            "rownumber": self.cursor.rownumber,
            "arraysize": self.cursor.arraysize,
            "lastrowid": self.cursor.lastrowid
        }
    
    async def get_last_id_from_table(self, table_name: str) -> int:
        return int((await self.pull(f'SELECT MAX(id) FROM {table_name}'))[0]['MAX(id)'])

    def __getattr__(self, name):
        return getattr(self.cursor, name)

class CursorContextManager:

    def __init__(self, pool: aiomysql.Pool) -> None:
        self.pool = pool

    async def __aenter__(self) -> CursorWrapper:
        self.connection = await self.pool.acquire()
        self.cursor = await self.connection.cursor()
        return CursorWrapper(self.cursor)
    
    async def __aexit__(self, *args) -> None:
        await self.cursor.close()
        await self.connection.commit()
        self.pool.release(self.connection)

class MysqlClient:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    async def connect(self) -> None:
        config_with_cursor = {**SQL_CONFIG, 'cursorclass': aiomysql.DictCursor}
        self.pool = await aiomysql.create_pool(**config_with_cursor)

    def __init__(self)  -> None:
        if not hasattr(self, "__initialized"): #for singleton (self.pool = None) must execute once
            self.pool = None
            self.__initialized = True


    async def disconnect(self) -> None:
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    def cursor(self) -> CursorContextManager:
        return CursorContextManager(self.pool)

mysql_client = MysqlClient()



class RedisClient:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        if not hasattr(self, "__initialized"): #for singleton (must execute once)
            self.redis = None
            self.pubsub = None
            self.listener_task = None
            self.__initialized = True

        self.__key_callbacks: dict[str, ExpireCallback] = {}

    async def connect(self):
        try:
            self.redis = await redis.from_url(REDIS_CONFIG['redis_url'])
            await self.redis.config_set('notify-keyspace-events', 'Ex')
            self.pubsub = self.redis.pubsub()
        except Exception as e:
            print(e)

    async def disconnect(self):
        if self.listener_task:
            self.listener_task.cancel()
            self.listener_task = None
        if self.pubsub:
            await self.pubsub.aclose()
            self.pubsub = None
        if self.redis:
            await self.redis.aclose()
            self.redis = None

    async def set(self, key: str, value: str, expire: Optional[int] = None):
        if expire:
            await self.redis.setex(key, expire, value)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str) -> str:
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        return await self.redis.exists(key) > 0

    async def keys(self, pattern: str = "*"):
        return await self.redis.keys(pattern)
    
    def __find_callback_key_starts_with(self, key):
        for k in self.__key_callbacks:
            if key.startswith(k):
                return k
    
    async def listen_for_expired_keys(self):
        await self.pubsub.subscribe('__keyevent@0__:expired')

        async for message in self.pubsub.listen():
            if message['type'] == 'message':
                expired_key = message['data'].decode()
                key_to_callback = self.__find_callback_key_starts_with(expired_key)

                if key_to_callback is not None:
                    callback: ExpireCallback = self.__key_callbacks[key_to_callback]
                    #executing onexp function
                    try:
                        if inspect.iscoroutinefunction(callback): 
                            await callback(expired_key)  #async 
                        else:
                            callback(expired_key)  #sync 
                    except Exception as e:
                        print(f"Error in callback listen_for_expired_keys: {e}")
                    
    def add_expire_listener(self, start_key: str, callback: ExpireCallback):
        self.__key_callbacks[start_key] = callback
            
        
        if not self.listener_task:
            self.listener_task = asyncio.create_task(self.listen_for_expired_keys())
    
    def remove_expire_listener(self, start_key):
        self.__key_callbacks.pop(start_key, None)

redis_client = RedisClient()


class S3Client:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        if not hasattr(self, "__initialized"): #for singleton (must execute once)
            self.session = aiobotocore.get_session()
            self.__initialized = True

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **S3_CONFIG) as client:
            yield client

    async def upload_file(self, file: Union[bytes, BinaryIO], bucket_name: str, key: str) -> None:
        async with self.get_client() as client:
            await client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=file
            )

    def get_file_url(self, bucket_name: str, key: str) -> str:
        return f"https://{bucket_name}.s3.amazonaws.com/{key}"
