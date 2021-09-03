# -*- coding: utf-8 -*-
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
iterations = 100_000


def _d_k(p: bytes, s: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=s,
        iterations=iterations,
        backend=backend,
    )
    return b64e(kdf.derive(p))


def strenc(message: bytes, p: str, iterations: int = iterations) -> bytes:
    s = secrets.token_bytes(16)
    key = _d_k(p.encode(), s, iterations)
    return b64e(
        b"%b%b%b"
        % (
            s,
            iterations.to_bytes(4, "big"),
            b64d(Fernet(key).encrypt(message)),
        )
    )
