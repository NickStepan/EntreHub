import hashlib

def hash_data(data):
    """Хешування ID"""
    return hashlib.sha3_256(str(data).encode()).hexdigest()