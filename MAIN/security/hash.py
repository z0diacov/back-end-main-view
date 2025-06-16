import hashlib
from security.config import SALT

def hash_password(password: str) -> str:
    return hashlib.sha256((SALT + password).encode()).hexdigest()

def verify_password(hashed: str, password: str) -> bool:
    return hashed == hash_password(password)