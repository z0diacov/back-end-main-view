import pika
from security.config import RABBITMQ_CONFIG, RABBITMQ_DEFAULT_PASS, RABBITMQ_DEFAULT_USER

class RabbitMQClientSync:


    def __init__(self) -> None:
        self.connection = None
        self.channel = None

    def connect(self) -> None:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_CONFIG['host'],
                    port=RABBITMQ_CONFIG['port'],
                    virtual_host=RABBITMQ_CONFIG['virtual_host'],
                    credentials=pika.PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS)
                )
            )
            self.connection = connection
            self.channel = self.connection.channel()
        except Exception as e:
            print(e)

    def publish(self, queue: str, body) -> None:
        try:
            self.channel.queue_declare(queue=queue, durable=True)
            self.channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )
        except Exception as e:
            print(e)

    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()

rabbitmq_client_sync = RabbitMQClientSync()