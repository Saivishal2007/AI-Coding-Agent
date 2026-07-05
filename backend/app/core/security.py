import hmac
import secrets
from hashlib import sha256

from app.core.config import settings


def generate_token(byte_length: int = 32) -> str:
    return secrets.token_urlsafe(byte_length)


def sign_value(value: str) -> str:
    digest = hmac.new(settings.SECRET_KEY.encode("utf-8"), value.encode("utf-8"), sha256).hexdigest()
    return f"{value}.{digest}"


def verify_signed_value(signed_value: str) -> bool:
    try:
        value, provided_digest = signed_value.rsplit(".", 1)
    except ValueError:
        return False

    expected_digest = hmac.new(settings.SECRET_KEY.encode("utf-8"), value.encode("utf-8"), sha256).hexdigest()
    return hmac.compare_digest(provided_digest, expected_digest)
