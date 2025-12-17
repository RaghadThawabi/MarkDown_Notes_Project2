from datetime import datetime, timedelta
from jose import jwt,JWTError
from app.core.config import settings

SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES=settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):#here I send the user id
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
