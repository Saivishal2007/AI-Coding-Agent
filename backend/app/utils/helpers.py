import re
from datetime import UTC, datetime


def utc_now() -> datetime:
    return datetime.now(UTC)


def compact_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()
