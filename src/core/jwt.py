from fastapi import HTTPException
from jose import jwt, JWTError
from ..config import cfg
from datetime import datetime, timedelta, timezone


def create_access_token(data: dict):
    exp = datetime.now(timezone.utc) + timedelta(minutes=cfg.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = data.copy()
    token.update({'exp': exp})
    return jwt.encode(token, cfg.JWT_SECRET_KEY, algorithm=cfg.ALGORITHM)


def verify_token(token: str):
    try:
        if (user_data := jwt.decode(token, cfg.JWT_SECRET_KEY, algorithms=[cfg.ALGORITHM])) and len(user_data) > 1:
            return user_data
        raise HTTPException(401, 'Empty access token', {"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(401, 'Invalid access token', {"WWW-Authenticate": "Bearer"})

