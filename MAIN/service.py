from rabbitmq import rabbitmq_client
from security.config import RABBIT_QUEUES

class Mailer:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
        
    def __init__(self):
        pass

    #{'type': 'email_confirm', 'recipient': 'arspav.voron@gmail.com', 'data': {'button_link': 'https://...'}
    async def send_email(self, message_type: str, recipient: str, data: dict) -> None:
        await rabbitmq_client.publish(
            RABBIT_QUEUES['to_mailer'], {
                'recipient': recipient, 
                'type': message_type,
                'data': data
            }
        )

mailer = Mailer()