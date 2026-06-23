from fastapi import APIRouter, Depends, status, Query
from app.core.dependencies import RoleChecker, get_current_user
from app.db.session import get_db
from sqlalchemy.orm.session import Session
from app.models.user_model import User, UserRole
from app.models.application_model import ApplicationStatus
from app.services.application_services import ApplicationServices
from app.schemas.application_schemas import (
    ApplicationResponseModel,
    ApplicationUpdateStatusModel,
    AdminApplicationResponseModel,
)
from typing import List, Literal

application_router = APIRouter()
application_services = ApplicationServices()
require_student = RoleChecker([UserRole.STUDENT])
require_admin = RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN])


@application_router.post(
    "/{olympiad_id}",
    response_model=ApplicationResponseModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_student)],
)
def create_application(
    olympiad_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    return application_services.create_application(olympiad_id, user, session)


@application_router.get(
    "/olympiad/{olympiad_id}",
    response_model=ApplicationResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_student)],
)
def get_my_application(
    olympiad_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    return application_services.get_my_application(olympiad_id, user, session)


@application_router.get(
    "",
    response_model=List[ApplicationResponseModel],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_student)],
)
def get_my_applications(
    user: User = Depends(get_current_user),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    size: int = Query(10, ge=1, le=100, description="Number of records to show"),
    session: Session = Depends(get_db),
):
    return application_services.get_my_applications(user, offset, size, session)


@application_router.patch(
    "/{application_id}/status",
    response_model=AdminApplicationResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin)],
)
def update_application_status(
    status_data: ApplicationUpdateStatusModel,
    application_id: int,
    session: Session = Depends(get_db),
):
    return application_services.update_application_status(
        status_data, application_id, session
    )


@application_router.get(
    "/admin/applications",
    response_model=List[AdminApplicationResponseModel],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin)],
)
def get_all_applications(
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    size: int = Query(10, ge=1, le=100, description="Number of records to show"),
    session: Session = Depends(get_db),
    order: Literal["asc" , "desc"] = Query('asc', description="Sort order"),
    status :  ApplicationStatus | None = Query(None, description="Filter by application status"),
    olympiad_id:int | None  = Query(None, ge=1,description="Filter by olympiad id"),
    sort_by: Literal["olympiad_id","created_at" ,"status"] | None = Query(None, description="Field used for sorting")
):
    return application_services.get_all_applications(offset=offset, size=size, session=session, olympiad_id= olympiad_id, status=status, sort_by=sort_by, order=order)



@application_router.get(
    "/admin/{application_id}",
    response_model=AdminApplicationResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin)],
)
def get_application_by_id(application_id: int, session: Session = Depends(get_db)):
    return application_services.get_application_by_id(application_id, session)
