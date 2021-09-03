# -*- coding: utf-8 -*-
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
_i = 100_000


def _d_k(p: bytes, s: bytes, _i: int = _i) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=s, iterations=_i, backend=backend
    )
    return b64e(kdf.derive(p))


def strdec(token: bytes, p: str) -> bytes:
    decoded = b64d(token)
    s, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    _i = int.from_bytes(iter, "big")
    key = _d_k(p.encode(), s, _i)
    return Fernet(key).decrypt(token)
