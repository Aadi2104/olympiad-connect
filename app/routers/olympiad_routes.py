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
from typing import List, Literal

require_admin_or_super_admin = RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN])
olympiad_services = OlympiadServices()

olympiad_router = APIRouter()


@olympiad_router.post(
    "",
    response_model=OlympiadResponseModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin_or_super_admin)],
)
def create_olympiad(
    olympiad_data: OlympiadCreateModel,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    return olympiad_services.create_olympiad(olympiad_data, current_user, session)


@olympiad_router.get(
    "/{olympiad_id}",
    response_model=OlympiadResponseModel,
    status_code=status.HTTP_200_OK,
)
def get_olympiad(olympiad_id: int, session: Session = Depends(get_db)):
    return olympiad_services.get_olympiad_by_id(olympiad_id, session)


@olympiad_router.get(
    "", response_model=List[OlympiadResponseModel], status_code=status.HTTP_200_OK
)
def get_all_olympiads(
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    size: int = Query(10, ge=1, le=100, description="Number of records to return"),
    title: str | None = Query(None, description="Filter olympiads by title"),
    is_active: bool | None = Query(None, description="Filter by active status"),
    sort_by: (
        Literal[
            "title", "created_at", "registration_start", "registration_end", "exam_date"
        ]
        | None
    ) = Query(None, description="Field used for sorting"),
    order: Literal["asc", "desc"] = Query("asc", description="Sort order"),
    session: Session = Depends(get_db),
):
    return olympiad_services.get_all_olympiads(
        offset=offset,
        size=size,
        session=session,
        order=order,
        title=title,
        is_active=is_active,
        sort_by=sort_by,
    )


@olympiad_router.patch(
    "/{olympiad_id}",
    response_model=OlympiadResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin_or_super_admin)],
)
def update_olympiad(
    olympiad_data: OlympiadUpdateModel,
    olympiad_id: int,
    session: Session = Depends(get_db),
):
    return olympiad_services.update_olympiad(olympiad_id, olympiad_data, session)


@olympiad_router.patch(
    "/{olympiad_id}/deactivate",
    response_model=OlympiadDeleteResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin_or_super_admin)],
)
def deactivate_olympiad(olympiad_id: int, session: Session = Depends(get_db)):
    return olympiad_services.deactivate_olympiad(olympiad_id, session)


@olympiad_router.patch(
    "/{olympiad_id}/activate",
    response_model=OlympiadResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin_or_super_admin)],
)
def activate_olympiad(olympiad_id: int, session: Session = Depends(get_db)):
    return olympiad_services.reactivate_olympiad(olympiad_id, session)
