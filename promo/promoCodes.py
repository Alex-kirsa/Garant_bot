import random
import string


def generate_promo_code(amount=1, length=6):
    letters = string.ascii_uppercase + string.digits + string.ascii_lowercase
    cod = []
    for x in range(amount):
        cod.append(''.join(random.choice(letters) for _ in range(length)))
    return cod


