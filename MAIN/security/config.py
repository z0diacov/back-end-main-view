import os

SECRET_KEY = ":)"
ALGORITHM = 'HS256'

ACCESS_TOKEN_EXPIRE_MINUTES = 10
ACCESS_TOKEN_EXPIRE_SECONDS = ACCESS_TOKEN_EXPIRE_MINUTES * 60

REFRESH_TOKEN_EXPIRE_DAYS = 7
REFRESH_TOKEN_EXPIRE_HOURS = REFRESH_TOKEN_EXPIRE_DAYS * 24
REFRESH_TOKEN_EXPIRE_MINUTES = REFRESH_TOKEN_EXPIRE_HOURS * 60
REFRESH_TOKEN_EXPIRE_SECONDS = REFRESH_TOKEN_EXPIRE_MINUTES * 60

EMAIL_CONFIRM_TOKEN_EXPIRE_MINUTES = 5
EMAIL_CONFIRM_TOKEN_EXPIRE_SECONDS = EMAIL_CONFIRM_TOKEN_EXPIRE_MINUTES * 60

RESET_PASSWORD_TOKEN_EXPIRE_MINUTES = 5
RESET_PASSWORD_TOKEN_EXPIRE_SECONDS = RESET_PASSWORD_TOKEN_EXPIRE_MINUTES * 60

GOOGLE_PASSWORD_TOKEN_EXPIRE_MINUTES = 5
GOOGLE_ADD_PASSWORD_TOKEN_EXPIRE_SECONDS = GOOGLE_PASSWORD_TOKEN_EXPIRE_MINUTES * 60

SALT = ':)'

# avatar
AVATAR_SIZE_LIMIT_IN_BYTES = 5 * 1024 * 1024  # 5 MB
ALLOWED_AVATAR_TYPES = [
    'image/jpeg',
    'image/png'
]

# OTP
OTP_SYMBOLS = '0123456789'
OTP_LENGTH = 6
OTP_EXPIRE_MINUTES = 2
OTP_EXPIRE_SECONDS = OTP_EXPIRE_MINUTES * 60

BACK_END_HOST = os.environ.get('BACK_END_HOST', 'http://localhost:8000')
FRONT_END_HOST = os.environ.get('FRONT_END_HOST', 'http://localhost:3000')

SQL_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': 'root',
    'password': 'root',
    'db': 'db',
    'minsize': 1,
    'maxsize': 10
}

REDIS_CONFIG = {
    'host': os.environ.get('CACHE_HOST', 'localhost'),
    'port': int(os.environ.get('CACHE_PORT', 6379)),
    'decode_responses': True
}

REDIS_CONFIG['redis_url'] = f"redis://{REDIS_CONFIG['host']}:{REDIS_CONFIG['port']}"


LOGGER_CONFIG = {
    'rotation': '10 MB',
    'retention': '7 days',
    'level': 'TRACE',
    'sink': os.environ.get('LOGGER_SINK', "../LOGS/app-logs/fastapi.log")
}

RABBITMQ_CONFIG = {
    'host': os.environ.get('RABBITMQ_HOST', 'localhost'),
    'port': int(os.environ.get('RABBITMQ_PORT', 5672)),
    'virtual_host': os.environ.get('RABBITMQ_DEFAULT_VHOST', '/'),
    'login': os.environ.get('RABBITMQ_DEFAULT_USER', 'root'),
    'password': os.environ.get('RABBITMQ_DEFAULT_PASS', 'root')
}

RABBIT_QUEUES = {
    'to_mailer': 'MAIN_MAILER',
    'to_media': 'MAIN_MEDIA',
}

GOOGLE_OAUTH_CONFIG =  {
    'redirect_uri': f'{FRONT_END_HOST}/api/oauth/google/callback',
    'client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID','444234478754-p231arcj90pu6pd1n45h3ge3l1gkuigh.apps.googleusercontent.com'),
    'client_secret': os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET', None)
}

S3_CONFIG = {
    'aws_access_key_id': os.environ.get('S3_ACCESS_KEY', ""),
    'aws_secret_access_key': os.environ.get('S3_SECRET_KEY', ""),
    'endpoint_url': os.environ.get('S3_ENDPOINT_URL', "")
}

S3_BUCKETS = {
    'avatars': ""
}