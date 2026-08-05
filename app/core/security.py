import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext

from app.core.config import settings
from app.core.errors import InvalidToken, TokenExpired
from app.models.user_model import User

signup_serializer = URLSafeTimedSerializer(
    secret_key=settings.SECRET_KEY, salt="signup-verification"
)

reset_password_serializer = URLSafeTimedSerializer(
    secret_key=settings.SECRET_KEY, salt="forgot-password"
)

passwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(user: User) -> str:
    payload_data = {
        "sub": str(user.id),
        "type": "access",
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_MINUTES),
        "role": user.role.value,
        "iss": settings.JWT_ISSUER,
    }
    token = jwt.encode(
        payload=payload_data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return token


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        token_data = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            issuer=settings.JWT_ISSUER,
        )
        if token_data.get("type") != "access":
            raise InvalidToken("Invalid Token Type")
        return token_data
    except ExpiredSignatureError:
        raise TokenExpired("Access token has expired")
    except InvalidTokenError:
        raise InvalidToken("Invalid access token")


def create_refresh_token(user: User) -> str:

    payload_data = {
        "sub": str(user.id),
        "type": "refresh",
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRY_DAYS),
        "role": user.role.value,
        "iss": settings.JWT_ISSUER,
    }

    token = jwt.encode(
        payload=payload_data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return token


def decode_refresh_token(token: str) -> dict[str , Any]:
    try:

        token_data = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            issuer=settings.JWT_ISSUER,
        )
        if token_data.get("type") != "refresh":
            raise InvalidToken("Invalid token type")
        
        return token_data
    except ExpiredSignatureError:
        raise TokenExpired("Refresh token has expired")
    except InvalidTokenError:
        raise InvalidToken("Invalid refresh token")


def generate_signup_token(data: dict[str, Any]) -> str:
    return signup_serializer.dumps(data)


def verify_signup_token(token: str) -> dict[str, Any]:
    try:
        return signup_serializer.loads(
            token, max_age=settings.SIGNUP_TOKEN_EXPIRY_MINUTES * 60
        )
    except SignatureExpired:
        raise TokenExpired("Signup token has expired")
    except BadSignature:
        raise InvalidToken("Invalid signup token")


def generate_otp() -> str:
    return str(secrets.randbelow(900000) + 100000)


def generate_reset_password_token(data: dict[str, Any]) -> str:
    return reset_password_serializer.dumps(data)


def verify_reset_password_token(token: str) -> dict[str, Any]:
    try:
        return reset_password_serializer.loads(
            token, max_age=settings.RESET_PASSWORD_TOKEN_EXPIRY_MINUTES * 60
        )
    except SignatureExpired:
        raise TokenExpired("Reset Password token has expired")
    except BadSignature:
        raise InvalidToken("Invalid reset password token")
