import aio_pika
import json
from security.config import RABBITMQ_CONFIG
import asyncio

class RabbitMQClient:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self) -> None:
        if not hasattr(self, '__initialized'):
            self.connection = None
            self.channel = None
            self.__initialized = True

    async def connect(self) -> None:
        try:
            loop = asyncio.get_event_loop()
            self.connection = await aio_pika.connect_robust(
                host=RABBITMQ_CONFIG['host'],
                port=RABBITMQ_CONFIG['port'],
                virtual_host=RABBITMQ_CONFIG['virtual_host'],
                login=RABBITMQ_CONFIG['login'],
                password=RABBITMQ_CONFIG['password'],
                loop=loop
            )
            self.channel = await self.connection.channel()
        except Exception as e:
            print(e)

    async def publish(self, queue: str, body: dict) -> None:
        try:
            json_body = json.dumps(body)
            body_bytes = json_body.encode('utf-8')

            await self.channel.declare_queue(queue, durable=True)
            await self.channel.default_exchange.publish(
                aio_pika.Message(body=body_bytes, delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
                routing_key=queue
            )
        except Exception as e:
            print(e)
    
    async def add_consumer(self, queue: str, callback):
        try:
            queue = await self.channel.declare_queue(queue, durable=True)
            await queue.consume(callback)
        except Exception as e:
            print(e)

    async def disconnect(self) -> None:
        if self.connection:
            await self.connection.close()

rabbitmq_client = RabbitMQClient()