from fastapi import APIRouter, status, Depends
from app.schemas.analytics_schema import DashboardAnalyticsResponseModel
from app.core.dependencies import RoleChecker
from app.db.session import get_db
from app.models.user_model import UserRole
from sqlalchemy.orm.session import Session
from app.services.analytics_services import AnalyticsServices


analytics_services = AnalyticsServices()
admin_required = RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN])

analytics_router = APIRouter()


@analytics_router.get("",response_model=DashboardAnalyticsResponseModel,status_code=status.HTTP_200_OK, dependencies=[Depends(admin_required)])
def get_dashboard_metrics(session:Session=Depends(get_db)):
    return analytics_services.get_dashboard_metrics(session)