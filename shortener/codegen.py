import random
import string

from django.conf import settings


def generate_code() -> str:
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(settings.DEFAULT_CODE_LENGTH))
