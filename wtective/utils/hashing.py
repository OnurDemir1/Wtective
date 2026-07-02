import mmh3
import base64


def get_favicon_hash(favicon_bytes: bytes) -> int:
    if not favicon_bytes:
        return None
    encoded = base64.encodebytes(favicon_bytes)
    return mmh3.hash(encoded)
