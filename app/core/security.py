from passlib.context import CryptContext
import jwt
from app.models.user_model import User
from app.core.config import settings
from datetime import datetime,timedelta,UTC
from itsdangerous import URLSafeTimedSerializer , BadSignature, SignatureExpired
from app.core.errors import InvalidToken,TokenExpired
from typing import Any
import secrets

signup_serializer = URLSafeTimedSerializer(
    secret_key=settings.SECRET_KEY,
    salt="signup-verification"
)

reset_password_serializer = URLSafeTimedSerializer(
    secret_key=settings.SECRET_KEY,
    salt="forgot-password"
)

passwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password:str):
    return passwd_context.hash(password)


def verify_password(password:str, hash:str)->bool:
    return passwd_context.verify(password,hash)


def create_access_token(user:User)->str:
    payload_data ={
        "user_id":user.id,
        "user_role":user.role.value,
        "exp": datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_MINUTES)
    }  
    token = jwt.encode(payload=payload_data,
                       key=settings.SECRET_KEY,
                       algorithm=settings.ALGORITHM
                       )
    return token

def decode_access_token(token:str)->dict:
    user_data=jwt.decode(token,
                        key=settings.SECRET_KEY,
                        algorithms=[settings.ALGORITHM])
    return user_data

def generate_signup_token(data:dict[str,Any]) -> str:
    return signup_serializer.dumps(data)


def verify_signup_token(token:str) -> dict[str,Any]:
    try:
        return signup_serializer.loads(token,max_age = settings.SIGNUP_TOKEN_EXPIRY_MINUTES * 60)
    except SignatureExpired:
        raise TokenExpired("Signup token has expired")
    except BadSignature:
        raise InvalidToken("Invalid signup token")
    
    
def generate_otp():
    return str(secrets.randbelow(900000)+100000)

def generate_reset_password_token(data:dict[str,Any]) -> str:
    return reset_password_serializer.dumps(data)

def verify_reset_password_token(token:str) -> dict[str,Any]:
    try:
         return reset_password_serializer.loads(token,max_age = settings.RESET_PASSWORD_TOKEN_EXPIRY_MINUTES * 60)
    except SignatureExpired:
        raise TokenExpired("Reset Password token has expired")
    except BadSignature:
        raise InvalidToken("Invalid reset password token")
        