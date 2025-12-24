from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Convert to bytes
    password_bytes = password.encode('utf-8')
    
    # Truncate to 72 bytes if necessary (bcrypt limitation)
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        # Decode back to string, ignoring any incomplete characters
        password = password_bytes.decode('utf-8', errors='ignore')
    
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Apply same truncation for verification
    password_bytes = plain_password.encode('utf-8')
    
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        plain_password = password_bytes.decode('utf-8', errors='ignore')
    
    return password_context.verify(plain_password, hashed_password)
