from fastapi import APIRouter, Depends, status, Query
from app.core.dependencies import get_current_user, RoleChecker
from app.db.session import get_db
from app.schemas.olympiad_schemas import (
    OlympiadCreateModel,
    OlympiadResponseModel,
    OlympiadUpdateModel,
    OlympiadDeleteResponseModel,
)
from sqlalchemy.orm.session import Session
from app.models.user_model import User, UserRole
from app.services.olympiad_services import OlympiadServices
from typing import List

role_checker = RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN])
olympiad_services = OlympiadServices()

olympiad_router = APIRouter()


@olympiad_router.post(
    "/create",
    response_model=OlympiadResponseModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(role_checker)],
)
def create_olympiad(
    olympiad_data: OlympiadCreateModel,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    return olympiad_services.create_olympiad(olympiad_data, current_user, session)


@olympiad_router.get(
    "/get/{olympiad_id}",
    response_model=OlympiadResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(role_checker)],
)
def get_olympiad_by_id(olympiad_id: int, session: Session = Depends(get_db)):
    return olympiad_services.get_olympiad_by_id(olympiad_id, session)


@olympiad_router.get(
    "/get-all",
    response_model=List[OlympiadResponseModel],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(role_checker)],
)
def get_all_olympiads(
    offset: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_db),
):
    return olympiad_services.get_all_olympiads(offset, size, session)


@olympiad_router.patch(
    "/update/{olympiad_id}",
    response_model=OlympiadResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(role_checker)],
)
def update_olympiad(
    olympiad_data: OlympiadUpdateModel,
    olympiad_id: int,
    session: Session = Depends(get_db),
):
    return olympiad_services.update_olympiad(olympiad_id, olympiad_data, session)


@olympiad_router.delete(
    "/deactivate/{olympiad_id}",
    response_model=OlympiadDeleteResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(role_checker)],
)
def deactivate_olympiad(olympiad_id: int, session: Session = Depends(get_db)):
    return olympiad_services.deactivate_olympiad(olympiad_id, session)


@olympiad_router.patch(
    "/reactivate/{olympiad_id}",
    response_model=OlympiadResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(role_checker)],
)
def reactivate_olympiad(olympiad_id: int, session: Session = Depends(get_db)):
    return olympiad_services.reactivate_olympiad(olympiad_id, session)
