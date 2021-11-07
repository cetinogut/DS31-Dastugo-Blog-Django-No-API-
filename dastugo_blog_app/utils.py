import uuid
import random


def get_random_code():
    code = str(uuid.uuid4())[:11].replace("-", "") # replace - with "" if exist
    return code

def get_random_digit():
    digit = random.randint(1,9)
    return digit