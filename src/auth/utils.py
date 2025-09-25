from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from src.config import Config
import uuid
import logging

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRY = timedelta(seconds=3600)  # 1 hour in seconds in time delta format


def generate_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
) -> str:
    payload = {}
    payload["user"] = user_data
    payload["exp"] = (
        datetime.now() + expiry
        if expiry is not None
        else datetime.now() + ACCESS_TOKEN_EXPIRY
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh
    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )
    return token


def decode_access_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
    except jwt.InvalidTokenError as e:
        logging.exception(e)
        return None
