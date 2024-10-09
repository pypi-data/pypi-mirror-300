import hashlib

def enc(data):
    """Encrypt data using SHA-256 hashing (irreversible)."""
    hashed_data = hashlib.sha256(data.encode()).hexdigest()
    return hashed_data
