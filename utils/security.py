import bcrypt

def hash_password(password: str) -> str:
    """Hash a password using bcrypt and return the UTF-8 decoded string."""
    # bcrypt.hashpw expects bytes and returns bytes
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plain password against a bcrypt hashed password."""
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
