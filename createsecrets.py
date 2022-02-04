#!/usr/bin/env python3
import secrets
from pathlib import Path

path = Path(".secrets")
path.mkdir(exist_ok=True)
for fname in ("django_secret_key.txt", "postgres_password.txt"):
    with open(path / fname, mode="x") as f:
        f.write(secrets.token_urlsafe(64))
