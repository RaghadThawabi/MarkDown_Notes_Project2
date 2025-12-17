from passlib.context import CryptContext
password_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return password_context.hash(password)

#to verify when user logs in
def verify_password(password, hashed_password):
    return password_context.verify(password, hashed_password)
