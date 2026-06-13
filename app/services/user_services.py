from app.schemas.user_schemas import UserCreateModel,UserLoginModel, UserVerifyModel, UserForgotPasswordModel, UserResetPasswordModel, UserManagementModel, UserLoginResponseModel , MessageResponseModel
from sqlalchemy.orm.session import Session
from app.models.user_model import User,UserRole
from app.core.errors import UserAlreadyExists,UserNotExist,InvalidCredentials, OTPRequired, InvalidOTP, InvalidPassword , UserAlreadyHasRole, SuperAdminModificationNotAllowed, UserStatusConflict
from app.core.security import (hash_password,verify_password,create_access_token,generate_otp,generate_signup_token,verify_signup_token,generate_reset_password_token,verify_reset_password_token)
from app.services.mail_services import Mail
from pydantic import EmailStr
from fastapi import BackgroundTasks
from typing import List

mail_service = Mail()

class UserServices:
    def get_user(self,user_id:int,session:Session)-> User:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotExist()
        return user
        
    
    def get_all_users(self,offset:int,size:int,session:Session)->List[User]:
        return session.query(User).filter(User.is_active.is_(True)).offset(offset).limit(size).all()
        
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
            data = {
                "email":user_email,
                "password_hash":hash_password(user_password),
                "otp":otp
            }
            token = generate_signup_token(data)
            
            mail_service.send_signup_mail(token,otp,[user_email],bg_tasks)
            
            return {
                "message": "If an account exists, a verification email has been sent"
            }
            
            
    def verify_user(self,otp_data:UserVerifyModel,token:str,session:Session)->User:
        try:
            data = verify_signup_token(token)
            if not otp_data.otp:
                raise OTPRequired()
            if data["otp"] != otp_data.otp:
                raise InvalidOTP()
            user = self.get_user_by_email(data["email"],session)
            if user:
                raise UserAlreadyExists()
            
            new_user = User(
                email=data["email"],
                password_hash=data["password_hash"]
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
        
        token = create_access_token(user)
        return {
            "access_token": token
        }

    
    def request_password_reset(self,email_data:UserForgotPasswordModel,bg_tasks:BackgroundTasks,session:Session) -> MessageResponseModel:
        
        
        user_email = email_data.email
        
        self.ensure_user_exists(user_email,session)
        
        
        data = {"email" : user_email}
        token = generate_reset_password_token(data)
        
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
        
    def get_all_admins(self,offset:int,size:int,session:Session) -> List[User]:
        return session.query(User).filter(User.is_active.is_(True),User.role == UserRole.ADMIN).offset(offset).limit(size).all()
        
            
            
        