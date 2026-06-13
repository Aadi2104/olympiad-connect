from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.user_model import UserRole


class UserCreateModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    
class UserVerifyModel(BaseModel):
    otp:str


class UserResponseModel(BaseModel):
    id: int
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class MessageResponseModel(BaseModel):
    message:str
    
class UserForgotPasswordModel(BaseModel):
    email:EmailStr
    
class UserResetPasswordModel(BaseModel):
    password:str = Field(min_length=8)
    confirm_password:str =  Field(min_length=8)
    
class UserManagementModel(BaseModel):
    user_id: int
    
class UserLoginResponseModel(BaseModel):
    access_token: str