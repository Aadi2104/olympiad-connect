from fastapi import APIRouter,Depends,status
from app.core.dependencies import RoleChecker,get_current_user
from app.db.session import get_db
from sqlalchemy.orm.session import Session
from app.models.user_model import User,UserRole
from app.services.application_services import ApplicationServices
from app.schemas.application_schemas import ApplicationResponseModel, ApplicationUpdateStatusModel , AdminApplicationResponseModel
from typing import List

application_router=APIRouter()
application_services=ApplicationServices()
student_role_checker = RoleChecker([UserRole.STUDENT])
admin_role_checker=RoleChecker([UserRole.ADMIN,UserRole.SUPER_ADMIN])

@application_router.post("/{olympiad_id}",response_model=ApplicationResponseModel,status_code=status.HTTP_201_CREATED,dependencies=[Depends(student_role_checker)])
def create_application(olympiad_id:int,user:User=Depends(get_current_user),session:Session=Depends(get_db)):
    return application_services.create_application(olympiad_id,user,session)

@application_router.get("/{olympiad_id}",response_model=ApplicationResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(student_role_checker)])
def get_my_application(olympiad_id:int, user:User=Depends(get_current_user),session:Session=Depends(get_db)):
    return application_services.get_my_application(olympiad_id,user,session)

@application_router.get("/",response_model=List[ApplicationResponseModel],status_code=status.HTTP_200_OK,dependencies=[Depends(student_role_checker)])
def get_my_applications(user:User=Depends(get_current_user),session:Session=Depends(get_db)):
        return application_services.get_my_applications(user,session)
    

@application_router.patch("/update-status/{application_id}",response_model=AdminApplicationResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def update_application_status(status:ApplicationUpdateStatusModel,application_id:int,session:Session=Depends(get_db)):
    return application_services.update_application_status(status,application_id,session)

@application_router.get("/admin/all",response_model=List[AdminApplicationResponseModel],status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def get_all_applications(session:Session=Depends(get_db)):
    return application_services.get_all_applications(session)

@application_router.get("/admin/olympiad/{olympiad_id}",response_model=List[AdminApplicationResponseModel],status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def get_applications_by_olympiad(olympiad_id:int,session:Session=Depends(get_db)):
    return application_services.get_applications_by_olympiad(olympiad_id,session)

@application_router.get("/admin/pending",response_model=List[AdminApplicationResponseModel],status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def get_pending_applications(session:Session=Depends(get_db)):
    return application_services.get_pending_applications(session)

@application_router.get("/admin/{application_id}",response_model=AdminApplicationResponseModel,status_code=status.HTTP_200_OK,dependencies=[Depends(admin_role_checker)])
def get_application_by_id(application_id:int,session:Session=Depends(get_db)):
    return application_services.get_application_by_id(application_id,session)
