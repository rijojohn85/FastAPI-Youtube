from datetime import datetime, timedelta
import uuid

import bcrypt
import jwt
from src.utils import logger

from src.config import Config

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(seconds=0), refresh: bool = False
) -> str:
    expiry_datetime = (
        (datetime.now() + expires_delta)
        if expires_delta is not None
        else datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    expiry = expiry_datetime.timestamp()
    payload = {
        "user": data,
        "exp": expiry,
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    logger.error(payload["exp"])
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM,
    )
    logger.error(decode_token(token))
    return token


def decode_token(token: str) -> dict | None:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logger.exception(e)
    return None


def verfiy_password_hash(password: str, password_hash: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash)
