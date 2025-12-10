from hashlib import blake2s


def get_key_hash(key: str) -> str:
    return blake2s(key.encode()).hexdigest()
