import random

def create_random_number_string(n: int) -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(n))
