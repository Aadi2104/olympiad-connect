from app.schemas.olympiad_schemas import OlympiadCreateModel, OlympiadUpdateModel
from sqlalchemy.orm.session import Session 
from sqlalchemy import desc
from app.models.olympiad_model import Olympiad
from app.models.user_model import User
from app.core.errors import (
    OlympiadNotExists,
    InvalidDateConfiguration,
    OlympiadAlreadyActive
)
from typing import List


class OlympiadServices:
    def get_olympiad(self, olympiad_id: int, session: Session) -> Olympiad:
        olympiad = (
            session.query(Olympiad)
            .filter(Olympiad.id == olympiad_id, Olympiad.is_active.is_(True))
            .first()
        )
        if olympiad is None:
            raise OlympiadNotExists()
        return olympiad

    def get_olympiad_by_id(self, olympiad_id: int, session: Session) -> Olympiad:
        olympiad = session.query(Olympiad).filter(Olympiad.id == olympiad_id).first()
        if olympiad is None:
            raise OlympiadNotExists()
        return olympiad

    def create_olympiad(
        self, olympiad_data: OlympiadCreateModel, current_user: User, session: Session
    ) -> Olympiad:
        try:

            new_olympiad = Olympiad(
                **olympiad_data.model_dump(), created_by_id=current_user.id
            )

            session.add(new_olympiad)
            session.commit()
            session.refresh(new_olympiad)
            return new_olympiad

        except Exception:
            session.rollback()
            raise

    def get_all_olympiads(
        self, offset: int, size: int, session: Session,order : str,  title: str | None = None, is_active: bool | None = None,
        sort_by : str | None = None
    ) -> List[Olympiad]:
        
        query = session.query(Olympiad)
        
        if title:
            query = query.filter(Olympiad.title.ilike(f"%{title}%"))
        if is_active is not None:
            query = query.filter(Olympiad.is_active == is_active)
        if sort_by:
            column = getattr(Olympiad, sort_by )
            if order.lower() == "desc":
                query = query.order_by(desc(column))
            else:
                query = query.order_by(column)
        else:
            query = query.order_by(desc(Olympiad.id))
                
        return query.offset(offset).limit(size).all()

    def update_olympiad(
        self, olympiad_id: int, olympiad_data: OlympiadUpdateModel, session: Session
    ) -> Olympiad:
        try:

            update_data = olympiad_data.model_dump(exclude_unset=True)
            olympiad = self.get_olympiad(olympiad_id, session)

            if not update_data:
                return olympiad

            registration_start = update_data.get(
                "registration_start", olympiad.registration_start
            )
            registration_end = update_data.get(
                "registration_end", olympiad.registration_end
            )
            exam_date = update_data.get("exam_date", olympiad.exam_date)

            if registration_start >= registration_end:
                raise InvalidDateConfiguration(
                    "Registration End date should be after registration start date"
                )

            if registration_end >= exam_date:
                raise InvalidDateConfiguration(
                    "Exam date should be after registration end date"
                )

            for key, value in update_data.items():
                setattr(olympiad, key, value)

            session.commit()
            session.refresh(olympiad)

            return olympiad

        except Exception:
            session.rollback()
            raise

    def deactivate_olympiad(self, olympiad_id: int, session: Session) -> Olympiad:
        try:
            olympiad = self.get_olympiad(olympiad_id, session)
            # if not olympiad.is_active:
            #     raise OlympiadAlreadyInactive()

            olympiad.is_active = False
            session.commit()
            session.refresh(olympiad)
            return olympiad
        except Exception:
            session.rollback()
            raise

    def reactivate_olympiad(self, olympiad_id: int, session: Session) -> Olympiad:
        try:
            olympiad = self.get_olympiad_by_id(olympiad_id, session)
            if olympiad.is_active:
                raise OlympiadAlreadyActive()
            olympiad.is_active = True
            session.commit()
            session.refresh(olympiad)
            return olympiad
        except Exception:
            session.rollback()
            raise
