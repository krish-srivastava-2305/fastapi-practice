import jwt 
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from app.config.env_secrets import get_env_variable

def create_jwt_token(id: str):
    secret = get_env_variable("JWT_SECRET")
    payload = {
        "sub": str(id),  # subject must be a string
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)  # timezone-aware
    }
    try:
        token = jwt.encode(payload, secret.strip(), algorithm="HS256")
        print("[SUCCESS] Token encoded:", token)
        return token
    except Exception as e:
        print("[ERROR] Failed to encode token:", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create JWT token"
        )

def decode_jwt_token(token: str):
    secret = get_env_variable("JWT_SECRET")
    print(f"[INFO] Decoding token: {repr(token)} and secret: {repr(secret)}")
    try:
        payload = jwt.decode(token, secret.strip(), algorithms=["HS256"])
        print("[SUCCESS] Payload:", payload)
        return payload
    except ExpiredSignatureError:
        print("[ERROR] Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )   
    except InvalidTokenError:
        print("[ERROR] Invalid token")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )
