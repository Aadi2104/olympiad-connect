from app.schemas.analytics_schema import DashboardAnalyticsResponseModel
from app.models.application_model import Application, ApplicationStatus
from app.models.olympiad_model import Olympiad
from app.models.student_profile_model import StudentProfile
from app.models.user_model import User, UserRole
from sqlalchemy.orm.session import Session
class AnalyticsServices:
    
    def get_dashboard_metrics(self, session:Session) -> DashboardAnalyticsResponseModel:
        
        total_users = session.query(User).count()
        total_students = session.query(User).filter(User.role == UserRole.STUDENT).count()
        total_admins = session.query(User).filter(User.role == UserRole.ADMIN).count()
        active_users = session.query(User).filter(User.is_active.is_(True)).count()

        total_olympiads = session.query(Olympiad).count()
        active_olympiads =  session.query(Olympiad).filter(Olympiad.is_active.is_(True)).count()
        
        total_applications = session.query(Application).count()
        pending_applications = session.query(Application).filter(Application.status == ApplicationStatus.PENDING).count()
        approved_applications = session.query(Application).filter(Application.status == ApplicationStatus.APPROVED).count()
        rejected_applications = session.query(Application).filter(Application.status == ApplicationStatus.REJECTED).count()
        approval_rate = (approved_applications / total_applications * 100
                        if total_applications > 0
                            else 0)
        approval_rate = round(approval_rate, 2)
        
        completed_profiles = session.query(StudentProfile).count()
            
        return DashboardAnalyticsResponseModel(

            total_users=total_users,
            total_students=total_students,
            total_admins=total_admins,
            active_users=active_users,
            total_olympiads=total_olympiads,
            active_olympiads=active_olympiads,
            total_applications=total_applications,
            pending_applications=pending_applications,
            approved_applications=approved_applications,
            rejected_applications=rejected_applications,
            completed_profiles=completed_profiles,
            approval_rate=approval_rate

                                                    ) 