import secrets

def generate(len=32):
    secret_key = secrets.token_hex(len)
    return secret_key

#print(generate(32))