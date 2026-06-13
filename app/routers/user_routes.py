from fastapi import APIRouter,status,Depends, BackgroundTasks, Query
from app.schemas.user_schemas import UserCreateModel,UserLoginModel,UserResponseModel, UserVerifyModel, MessageResponseModel, UserForgotPasswordModel, UserResetPasswordModel, UserManagementModel, UserLoginResponseModel
from app.db.session import get_db
from sqlalchemy.orm.session import Session
from app.services.user_services import UserServices
from app.models.user_model import User ,UserRole
from app.core.dependencies import get_current_user,RoleChecker
from typing import List



user_router=APIRouter()
user_services=UserServices()
role_checker= RoleChecker([UserRole.STUDENT,UserRole.ADMIN,UserRole.SUPER_ADMIN])
admin_role_checker = RoleChecker([UserRole.SUPER_ADMIN])

@user_router.post("/signup",response_model=MessageResponseModel,status_code=status.HTTP_202_ACCEPTED)
def initiate_user(user_data:UserCreateModel,bg_tasks:BackgroundTasks,session:Session=Depends(get_db)):
    return  user_services.initiate_signup(user_data,bg_tasks,session)

@user_router.post("/verify-signup/{token}",response_model=UserResponseModel,status_code=status.HTTP_201_CREATED)
def verify_signup(otp_data:UserVerifyModel,token:str,session:Session=Depends(get_db)):
    return user_services.verify_user(otp_data,token,session)
    
    
@user_router.post("/login",response_model=UserLoginResponseModel,status_code=status.HTTP_200_OK)
def login_user(user_data:UserLoginModel,session:Session=Depends(get_db)):
    return user_services.login_user(user_data,session)

@user_router.get("/me",response_model=UserResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(role_checker)])
def get_me(user:User=Depends(get_current_user)):
    return user


@user_router.get("/get-all",response_model=List[UserResponseModel],status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def get_all_users(offset:int = Query(0,ge=0), size:int = Query(10,ge=1,le=100),session:Session=Depends(get_db),):
    return user_services.get_all_users(offset,size,session)

@user_router.post("/forgot-password",response_model=MessageResponseModel,status_code=status.HTTP_200_OK)
def request_password_reset(email_data:UserForgotPasswordModel,bg_tasks:BackgroundTasks,session:Session=Depends(get_db)):
    return user_services.request_password_reset(email_data,bg_tasks,session)

@user_router.patch("/reset-password/{token}",response_model=MessageResponseModel,status_code=status.HTTP_200_OK)
def reset_password(password_data:UserResetPasswordModel,token:str,session:Session=Depends(get_db)):
    return user_services.reset_password(password_data,token,session)




@user_router.patch("/promote-admin",response_model=MessageResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def promote_admin(user_data:UserManagementModel,session:Session=Depends(get_db)):
    return user_services.promote_admin(user_data,session)

@user_router.patch("/demote-admin",response_model=MessageResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def demote_admin(user_data:UserManagementModel,session:Session=Depends(get_db)):
    return user_services.demote_admin(user_data,session)
@user_router.patch("/activate-user",response_model=MessageResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def activate_user(user_data:UserManagementModel,session:Session=Depends(get_db)):
    return user_services.activate_user(user_data,session)


@user_router.patch("/deactivate-user",response_model=MessageResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def deactivate_user(user_data:UserManagementModel,session:Session=Depends(get_db)):
    return user_services.deactivate_user(user_data,session)

@user_router.get("/get-all-admins",response_model=List[UserResponseModel],status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def get_all_admins(offset:int = Query(0,ge=0),size:int = Query(10,ge=1,le=100),session:Session=Depends(get_db),):
    return user_services.get_all_admins(offset,size,session)