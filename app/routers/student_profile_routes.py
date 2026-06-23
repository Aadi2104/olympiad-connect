from fastapi import APIRouter, Depends, status, Query
from app.schemas.student_profile_schemas import (
    StudentProfileCreateModel,
    StudentProfileResponseModel,
    StudentProfilePhoneNumberUpdateModel,
    AdminStudentProfileResponseModel,
)
from app.core.dependencies import get_current_user, RoleChecker
from app.db.session import get_db
from app.services.student_profile_services import StudentProfileServices
from app.models.user_model import User, UserRole
from app.models.student_profile_model import StudentGender
from sqlalchemy.orm.session import Session
from typing import List, Literal

student_profile_router = APIRouter()
student_profile_service = StudentProfileServices()
student_require = RoleChecker([UserRole.STUDENT])
admin_required = RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN])


@student_profile_router.post(
    "",
    response_model=StudentProfileResponseModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(student_require)],
)
def create_student_profile(
    student_data: StudentProfileCreateModel,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    return student_profile_service.create_student_profile(student_data, user, session)


@student_profile_router.get(
    "/me",
    response_model=StudentProfileResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(student_require)],
)
def get_profile(user: User = Depends(get_current_user)):
    return student_profile_service.get_student_profile(user)


@student_profile_router.patch(
    "/phone-number",
    response_model=StudentProfileResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(student_require)],
)
def update_phone_number(
    phone_data: StudentProfilePhoneNumberUpdateModel,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    return student_profile_service.update_phone_number(phone_data, user, session)


@student_profile_router.get(
    "/students/{student_id}",
    response_model=AdminStudentProfileResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_required)],
)
def get_student_by_id(student_id: int, session: Session = Depends(get_db)):
    return student_profile_service.get_student_by_id(student_id, session)


@student_profile_router.get(
    "/students",
    response_model=List[AdminStudentProfileResponseModel],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_required)],
)
def get_all_students(
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    size: int = Query(10, ge=1, le=100, description="Number of records to return"),
    session: Session = Depends(get_db),
    order: Literal["asc" , "desc"] = Query("asc" , description="Sorting order"),
    first_name: str | None = Query(None, description="Filter students by first name"),
    college_name: str | None = Query(None, description="Filter students by college name"),
    branch: str | None = Query(None, description="Filter students using branch"),
    semester: int | None = Query(None, description="Filter students using semster"),
    gender: StudentGender | None = Query(None, description="Filter students by gender"),
    sort_by: Literal[ "first_name", "college_name", "branch","semester", "gender", "updated_at"] | None = Query(None, description="Sorting Field"),
):
    return student_profile_service.get_all_students(offset = offset, size = size, session = session, order = order, first_name=first_name, 
                                                    college_name=college_name, branch=branch, semester=semester, gender=gender, sort_by=sort_by)
