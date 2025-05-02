import random
import string

def generate_password():
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = '#.,!@&^%*'

    length = random.randint(8, 16)

    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]

    all_chars = lowercase + uppercase + digits + special_chars
    password.extend(random.choice(all_chars) for _ in range(length - 4))

    random.shuffle(password)

    return ''.join(password)