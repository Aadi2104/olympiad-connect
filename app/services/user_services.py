from datetime import UTC, datetime, timedelta

from fastapi import BackgroundTasks
from pydantic import EmailStr
from sqlalchemy import desc
from sqlalchemy.orm.session import Session

from app.core.config import settings
from app.core.errors import (
    InvalidCredentials,
    InvalidOTP,
    InvalidPassword,
    OTPRequired,
    SuperAdminModificationNotAllowed,
    UserAlreadyExists,
    UserAlreadyHasRole,
    UserNotExist,
    UserStatusConflict,
    InvalidToken,
    RefreshTokenNotFound,
    RefreshTokenRevoked,
    TokenExpired
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    generate_otp,
    generate_reset_password_token,
    generate_signup_token,
    hash_password,
    hash_refresh_token,
    verify_password,
    verify_reset_password_token,
    verify_signup_token,
    verify_refresh_token,
    
)
from app.models.refresh_token_model import RefreshToken
from app.models.user_model import User, UserRole
from app.schemas.user_schemas import (
    MessageResponseModel,
    UserCreateModel,
    UserForgotPasswordModel,
    UserLoginModel,
    UserLoginResponseModel,
    UserManagementModel,
    UserResetPasswordModel,
    UserVerifyModel,
    UserLogoutModel
)
from app.services.mail_services import Mail

mail_service = Mail()

class UserServices:
    def get_user(self,user_id:int,session:Session)-> User:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotExist()
        return user
        
    
    def get_all_users(self,offset:int,size:int,session:Session, order:str, email : str | None = None, role : UserRole | None =None , is_active: bool | None = None, sort_by: str | None = None
)->list[User]:
        
        query = session.query(User)
        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))
        if role:
            query = query.filter(User.role == role)
        if is_active is not None:
            query  = query.filter(User.is_active == is_active)
        if sort_by:
            column = getattr(User, sort_by)
            if order == "desc":
                query = query.order_by(desc(column))
            else:
                query = query.order_by(column)
        else:
            query = query.order_by(desc(User.id))
        return query.offset(offset).limit(size).all()
        
    def get_user_by_email(self,user_email:EmailStr,session:Session)->User | None:
        return  session.query(User).filter(User.email == user_email).first()
        
    def ensure_user_exists(self,user_email:EmailStr,session:Session)->User:
        user = self.get_user_by_email(user_email,session)
        if not user:
            raise UserNotExist()
        return user
        
    def initiate_signup(self,user_data:UserCreateModel,bg_tasks:BackgroundTasks,session:Session) -> MessageResponseModel:
            user_email=user_data.email
            user_password=user_data.password
            user = self.get_user_by_email(user_email,session)
            if user:
                raise UserAlreadyExists()
            
            otp = generate_otp()
            signup_data = {
                "email":user_email,
                "password_hash":hash_password(user_password),
                "otp":otp
            }
            token = generate_signup_token(signup_data)
            
            mail_service.send_signup_mail(token,otp,[user_email],bg_tasks)
            
            return {
                "message": "If an account exists, a verification email has been sent"
            }
            
            
    def verify_user(self,otp_data:UserVerifyModel,token:str,session:Session)->User:
        try:
            signup_data = verify_signup_token(token)
            if not otp_data.otp:
                raise OTPRequired()
            if signup_data["otp"] != otp_data.otp:
                raise InvalidOTP()
            user = self.get_user_by_email(signup_data["email"],session)
            if user:
                raise UserAlreadyExists()
            
            new_user = User(
                email=signup_data["email"],
                password_hash=signup_data["password_hash"]
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
        except Exception:
            session.rollback()
            raise
   
    def login_user(self,user_data:UserLoginModel,session:Session)->UserLoginResponseModel:
        user_email=user_data.email
        user_password = user_data.password
        
        user = self.ensure_user_exists(user_email,session)
        
        if not verify_password(user_password,user.password_hash):
            raise InvalidCredentials()
        
        access_token = create_access_token(user)
        refresh_token , jti= create_refresh_token(user)
        
        refresh_token_record = RefreshToken(
            user_id = user.id,
            jti = jti,
            token_hash =  hash_refresh_token(refresh_token),
            expires_at = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRY_DAYS)
        )
        try: 
            session.add(refresh_token_record)
            session.commit()
        except Exception:
            session.rollback()
            raise
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def logout_user(self,logout_data : UserLogoutModel, session:Session) -> MessageResponseModel:
        try:
            refresh_token = logout_data.refresh_token
            refresh_token_data = decode_refresh_token(refresh_token)
            
            refresh_token_jti = refresh_token_data["jti"]
            
            refresh_token_record = session.query(RefreshToken).filter(RefreshToken.jti == refresh_token_jti).first()
            
            if not refresh_token_record:
                raise RefreshTokenNotFound()
            
            if refresh_token_record.is_revoked:
                raise RefreshTokenRevoked()
            
            if refresh_token_record.expires_at < datetime.now():
                raise TokenExpired("Refresh token has expired")
            
            refresh_token_hash = refresh_token_record.token_hash
            
            if not verify_refresh_token(refresh_token , refresh_token_hash):
                raise InvalidToken("Invalid refresh token")
            
            refresh_token_record.is_revoked = True
            
            session.commit()
            return {
                "message" : "Logged out successfully"
            }
            
        except Exception:
            session.rollback()
            raise
        
        
        
    
    
    
    def request_password_reset(self,email_data:UserForgotPasswordModel,bg_tasks:BackgroundTasks,session:Session) -> MessageResponseModel:
        
        
        user_email = email_data.email
        
        self.ensure_user_exists(user_email,session)
        
        
        reset_password_data = {"email" : user_email}
        token = generate_reset_password_token(reset_password_data)
        
        mail_service.send_reset_password_mail(token,[email_data.email],bg_tasks)
        
        return {
            "message":"If an account exists, a password reset email has been sent"
        }
        
    def reset_password(self,password_data:UserResetPasswordModel,token:str,session:Session) -> MessageResponseModel:
        try:
            password = password_data.password
            
            confirm_password = password_data.confirm_password
            
            token_data = verify_reset_password_token(token)
            user_email = token_data["email"]
            
            if password != confirm_password:
                raise InvalidPassword()
            
            user = self.ensure_user_exists(user_email,session)
            
            user.password_hash=hash_password(password)
            
            session.commit()
            session.refresh(user)
            
            return {
                "message":"Password reset successfully"
            }
            
        except Exception:
            session.rollback()
            raise
        
        
    def activate_user(self,user_data:UserManagementModel,session:Session) -> MessageResponseModel:
        try:
            user = self.get_user(user_data.user_id,session)
            if user.role == UserRole.SUPER_ADMIN:
                raise SuperAdminModificationNotAllowed()
            if user.is_active:
                raise UserStatusConflict("User is already active")
            
            user.is_active = True
            session.commit()
            return{
                "message":"User activated successfully"
            }
        except Exception:
            session.rollback()
            raise
            
    def deactivate_user(self,user_data:UserManagementModel,session:Session) -> MessageResponseModel:
        try:
            user = self.get_user(user_data.user_id,session)
            if user.role == UserRole.SUPER_ADMIN:
                raise SuperAdminModificationNotAllowed()
            if not user.is_active:
                raise UserStatusConflict("User is already inactive")
            user.is_active = False
            session.commit()
            return{
                "message":"User deactivated successfully"
            }
        except Exception:
            session.rollback()
            raise
            
            
            
        
    
    def promote_admin(self,user_data:UserManagementModel,session:Session) ->MessageResponseModel:
        try:
            user = self.get_user(user_data.user_id,session)
            if not user.is_active:
                raise UserStatusConflict("Inactive users cannot be promoted to admin")
                
            if user.role == UserRole.ADMIN:
                raise UserAlreadyHasRole("User is already an admin")
            if user.role == UserRole.SUPER_ADMIN:
                raise SuperAdminModificationNotAllowed()
            user.role = UserRole.ADMIN
            session.commit()
            return {
                "message":"User promoted to admin successfully"
            }
        except Exception:
            session.rollback()
            raise
        
    def demote_admin(self,user_data:UserManagementModel,session:Session)-> MessageResponseModel:
        try:
            user = self.get_user(user_data.user_id,session)
            if not user.is_active:
                raise UserStatusConflict("Inactive users cannot be demoted to student")
            if user.role == UserRole.STUDENT:
                raise UserAlreadyHasRole("User is already a student")
            if user.role == UserRole.SUPER_ADMIN:
                raise SuperAdminModificationNotAllowed()
            
            user.role = UserRole.STUDENT
            session.commit()
            return {
                "message":"User demoted to student successfully"
            }
        except Exception:
            session.rollback()
            raise
        
    def get_all_admins(self,offset:int,size:int,session:Session) -> list[User]:
        return session.query(User).filter(User.is_active.is_(True),User.role == UserRole.ADMIN).offset(offset).limit(size).all()
        
    
            
        