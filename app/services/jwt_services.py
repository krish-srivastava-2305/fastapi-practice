from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status
from app.config.env_secrets import get_env_variable
from datetime import datetime, timedelta


def create_jwt_token(user_email: str) -> str:
    payload = {
        "sub": user_email,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    secret = get_env_variable("JWT_SECRET")
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


def decode_jwt_token(token: str) -> dict:
    secret = get_env_variable("JWT_SECRET")
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )