from fastapi import APIRouter, Depends , status
from app.schemas.student_profile_schemas import StudentProfileCreateModel,StudentProfileResponseModel, StudentProfilePhoneNumberUpdateModel , AdminStudentProfileResponseModel
from app.core.dependencies import get_current_user , RoleChecker
from app.db.session import get_db
from app.services.student_profile_services import StudentProfileServices
from app.models.user_model import User, UserRole
from sqlalchemy.orm.session import Session
from typing import List

student_profile_router = APIRouter()
student_profile_service=StudentProfileServices()
role_checker = RoleChecker([UserRole.STUDENT])
admin_role_checker=RoleChecker([UserRole.ADMIN,UserRole.SUPER_ADMIN])

@student_profile_router.post("/create",response_model=StudentProfileResponseModel,status_code=status.HTTP_201_CREATED,dependencies=[Depends(role_checker)])
def create_student_profile(student_data:StudentProfileCreateModel,user:User=Depends(get_current_user),session:Session=Depends(get_db)):
    return student_profile_service.create_student_profile(student_data,user,session)
    
@student_profile_router.get("/me",response_model=StudentProfileResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(role_checker)])
def get_profile(user:User=Depends(get_current_user)):
    return student_profile_service.get_student_profile(user)

@student_profile_router.patch('/phone-number',response_model=StudentProfileResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(role_checker)])
def update_phone_number(phone_number:StudentProfilePhoneNumberUpdateModel,user:User=Depends(get_current_user),session:Session=Depends(get_db)):
    return student_profile_service.update_phone_number(phone_number,user,session)

@student_profile_router.get("/{student_id}",response_model=AdminStudentProfileResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def get_student_by_id(student_id:int,session:Session=Depends(get_db)):
    return student_profile_service.get_student_by_id(student_id,session)

@student_profile_router.get("/",response_model=List[AdminStudentProfileResponseModel],status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def get_all_students(session:Session=Depends(get_db)):
    return student_profile_service.get_all_students(session)
