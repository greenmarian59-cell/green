from datetime import datetime, UTC, timedelta

import jwt
from pwdlib import PasswordHash
from src.config import settings

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def _create_token(user_id: int, token_type: str, expires_minutes: int) -> str:
    now = datetime.now(UTC)

    payload = {
        "sub": str(user_id),
        "type": token_type,
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def create_access_token(user_id: int) -> str:
    return _create_token(
        user_id,
        ACCESS_TOKEN_TYPE,
        settings.jwt_access_token_expired_minute,
    )


def create_refresh_token(user_id: int) -> str:
    return _create_token(
        user_id,
        REFRESH_TOKEN_TYPE,
        settings.jwt_refresh_token_expired_minute,
    )


def decode_token(token: str, expected_type: str = ACCESS_TOKEN_TYPE) -> dict:
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
        options={
            "require": ["exp", "iat", "sub"],
        },
    )

    if payload.get("type") != expected_type:
        raise jwt.InvalidTokenError(f"Expected {expected_type} token")

    return payload

async def get_user_id_from_token(
    token: str, expected_type: str = ACCESS_TOKEN_TYPE
) -> int:
    payload = decode_token(token, expected_type=expected_type)

    try:
        return int(payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise jwt.InvalidTokenError("Invalid subject claim") from exc