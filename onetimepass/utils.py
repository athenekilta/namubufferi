import secrets


def random_pin(width=6):
    return str(secrets.randbelow(10 ** width)).zfill(width)
