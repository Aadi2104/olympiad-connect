from app.models.user_model import User
from sqlalchemy.orm.session import Session
from app.models.application_model import Application, ApplicationStatus
from app.core.errors import (
    ApplicationAlreadyExists,
    OlympiadInactive,
    RegistrationNotStarted,
    RegistrationClosed,
    ApplicationNotExists,
    ProfileNotCompleted,
    OlympiadNotExists
)
from sqlalchemy.exc import IntegrityError
from app.services.olympiad_services import OlympiadServices
from datetime import datetime
from app.schemas.application_schemas import ApplicationUpdateStatusModel
from typing import List
from app.core.errors import ApplicationAlreadyReviewed

olympiad_services = OlympiadServices()


class ApplicationServices:
    def create_application(
        self, olympiad_id: int, user: User, session: Session
    ) -> Application:
        try:
            if user.student_profile is None:
                raise ProfileNotCompleted()

            olympiad = olympiad_services.get_olympiad(olympiad_id, session)
            if not olympiad.is_active:
                raise OlympiadInactive()

            if datetime.now() > olympiad.registration_end:
                raise RegistrationClosed()

            if datetime.now() < olympiad.registration_start:
                raise RegistrationNotStarted()

            new_application = Application(
                user_id=user.id,
                olympiad_id=olympiad_id,
            )

            session.add(new_application)
            session.commit()
            session.refresh(new_application)
            return new_application

        except IntegrityError:
            session.rollback()
            raise ApplicationAlreadyExists()

        except Exception:
            session.rollback()
            raise

    def get_my_application(
        self, olympiad_id: int, user: User, session: Session
    ) -> Application:
        application = (
            session.query(Application)
            .filter(
                Application.olympiad_id == olympiad_id, Application.user_id == user.id
            )
            .first()
        )
        if not application:
            raise ApplicationNotExists()
        return application

    def get_my_applications(self, user: User, offset:int, size:int, session: Session) -> List[Application]:
        applications = (
            session.query(Application).filter(Application.user_id == user.id).offset(offset).limit(size).all()
        )
        return applications

    def get_all_applications(self,offset:int, size:int, session: Session) -> List[Application]:
        applications = session.query(Application).offset(offset).limit(size).all()
        return applications

    def get_application_by_id(
        self, application_id: int, session: Session
    ) -> Application:
        application = (
            session.query(Application).filter(Application.id == application_id).first()
        )
        if not application:
            raise ApplicationNotExists()
        return application

    def update_application_status(
        self,
        status_data: ApplicationUpdateStatusModel,
        application_id: int,
        session: Session,
    ) -> Application:
        try:
            application = self.get_application_by_id(application_id, session)
            if application.status != ApplicationStatus.PENDING:
                raise ApplicationAlreadyReviewed()
            application.status = status_data.status
            session.commit()
            session.refresh(application)
            return application
            
        except Exception:
            session.rollback()
            raise
    
    def get_applications_by_olympiad(self,olympiad_id:int,offset:int, size:int,session:Session)->List[Application]:
        olympiad_services.get_olympiad(olympiad_id,session) 
        applications = session.query(Application).filter(Application.olympiad_id == olympiad_id).offset(offset).limit(size).all()
        return applications
        
        
    def get_pending_applications(self,offset:int, size:int,session:Session)->List[Application]:
        applications = session.query(Application).filter(Application.status == ApplicationStatus.PENDING).offset(offset).limit(size).all()
        return applications