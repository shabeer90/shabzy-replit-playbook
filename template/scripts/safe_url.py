"""Keep a URL from scraped or third-party data only if it's a plain https URL that can't break out of
an attribute or a script body, such as closing a JSON-LD script tag (stored XSS)."""
from urllib.parse import urlsplit

_UNSAFE = set('<>"\'` \t\r\n\\')


def safe_url(src):
    if not src:
        return None
    src = src.strip()
    if src.startswith("//"):
        src = "https:" + src
    if any(c in _UNSAFE for c in src):
        return None
    try:
        parts = urlsplit(src)
    except ValueError:
        return None
    return src if parts.scheme == "https" and parts.hostname else None
