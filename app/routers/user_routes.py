from fastapi import APIRouter,status,HTTPException,Depends, BackgroundTasks
from app.schemas.auth_schemas import UserCreateModel,UserLoginModel,UserResponseModel, UserVerifyModel, MessageResponseModel, UserForgotPasswordModel, UserResetPasswordModel, UserManagementModel
from app.db.session import get_db
from sqlalchemy.orm.session import Session
from app.services.user_sevices import AuthServices
from app.models.user_model import User ,UserRole
from app.core.dependencies import get_current_user,RoleChecker
from typing import List



user_router=APIRouter()
auth_service=AuthServices()
role_checker= RoleChecker([UserRole.STUDENT,UserRole.ADMIN,UserRole.SUPER_ADMIN])
admin_role_checker = RoleChecker([UserRole.SUPER_ADMIN])

@user_router.post("/signup",response_model=MessageResponseModel,status_code=status.HTTP_307_TEMPORARY_REDIRECT)
def initiate_user(user_data:UserCreateModel,bg_tasks:BackgroundTasks,session:Session=Depends(get_db)):
    return  auth_service.initiate_signup(user_data,bg_tasks,session)

@user_router.post("/verify-signup/{token}",response_model=UserResponseModel,status_code=status.HTTP_201_CREATED)
def verify_signup(otp_data:UserVerifyModel,token:str,session:Session=Depends(get_db)):
    return auth_service.verify_user(otp_data,token,session)
    
    
@user_router.post("/login",status_code=status.HTTP_200_OK)
def login_user(user_data:UserLoginModel,session:Session=Depends(get_db)):
    return auth_service.login_user(user_data,session)

@user_router.get("/me",response_model=UserResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(role_checker)])
def get_me(user:User=Depends(get_current_user),session:Session=Depends(get_db)):
    return user


@user_router.get("/get_all",response_model=List[UserResponseModel],status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def get_all_users(session:Session=Depends(get_db)):
    return auth_service.get_all_users(session)

@user_router.post("/forgot-password",response_model=MessageResponseModel,status_code=status.HTTP_200_OK)
def request_password_reset(email_data:UserForgotPasswordModel,bg_tasks:BackgroundTasks,session:Session=Depends(get_db)):
    return auth_service.request_password_reset(email_data,bg_tasks,session)

@user_router.patch("/reset-password/{token}",response_model=MessageResponseModel,status_code=status.HTTP_200_OK)
def reset_password(password_data:UserResetPasswordModel,token:str,session:Session=Depends(get_db)):
    return auth_service.reset_password(password_data,token,session)




@user_router.patch("/promote-admin",response_model=MessageResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def promote_admin(user_data:UserManagementModel,session:Session=Depends(get_db)):
    return auth_service.promote_admin(user_data,session)

@user_router.patch("/demote-admin",response_model=MessageResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def demote_admin(user_data:UserManagementModel,session:Session=Depends(get_db)):
    return auth_service.demote_admin(user_data,session)
@user_router.patch("/activate-user",response_model=MessageResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def activate_user(user_data:UserManagementModel,session:Session=Depends(get_db)):
    return auth_service.activate_user(user_data,session)


@user_router.patch("/deactivate-user",response_model=MessageResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def deactivate_user(user_data:UserManagementModel,session:Session=Depends(get_db)):
    return auth_service.deactivate_user(user_data,session)

@user_router.get("/get-all-admins",response_model=List[UserResponseModel],status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def get_all_admins(session:Session=Depends(get_db)):
    return auth_service.get_all_admins(session)