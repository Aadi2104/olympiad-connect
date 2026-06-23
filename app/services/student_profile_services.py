from sqlalchemy.orm.session import Session
from sqlalchemy import desc
from app.schemas.student_profile_schemas import (
    StudentProfileCreateModel,
    StudentProfilePhoneNumberUpdateModel,
)
from app.core.errors import (
    ProfileAlreadyExists,
    ProfileDataAlreadyExists,
    ProfileNotExists,
)
from app.models.user_model import User
from app.models.student_profile_model import StudentProfile, StudentGender
from sqlalchemy.exc import IntegrityError
from typing import List


class StudentProfileServices:
    def create_student_profile(
        self, student_data: StudentProfileCreateModel, user: User, session: Session
    ) -> StudentProfile:
        try:
            if user.student_profile:
                raise ProfileAlreadyExists()

            new_student_profile = StudentProfile(
                **student_data.model_dump(), user_id=user.id
            )

            session.add(new_student_profile)
            session.commit()
            session.refresh(new_student_profile)
            return new_student_profile
        except IntegrityError:
            session.rollback()
            raise ProfileDataAlreadyExists()

        except Exception:
            session.rollback()
            raise

    def get_student_profile(self, user: User) -> StudentProfile:
        if not user.student_profile:
            raise ProfileNotExists()
        student_profile = user.student_profile

        return student_profile

    def update_phone_number(
        self,
        phone_data: StudentProfilePhoneNumberUpdateModel,
        user: User,
        session: Session,
    ) -> StudentProfile:
        try:
            phone_number = phone_data.phone_number
            student_profile = self.get_student_profile(user)
            student_profile.phone_number = phone_number
            session.commit()
            session.refresh(student_profile)
        except IntegrityError:
            session.rollback()
            raise ProfileDataAlreadyExists()
        except Exception:
            session.rollback()
            raise

        return student_profile

    def get_student_by_id(self, student_id: int, session: Session) -> StudentProfile:
        student_profile = (
            session.query(StudentProfile)
            .filter(StudentProfile.id == student_id)
            .first()
        )
        if not student_profile:
            raise ProfileNotExists()
        return student_profile

    def get_all_students(
        self,
        offset: int,
        size: int,
        session: Session,
        order: str,
        first_name: str | None = None,
        college_name: str | None = None,
        branch: str | None = None,
        semester: int | None = None,
        gender: StudentGender | None = None,
        sort_by: str | None = None,
    ) -> List[StudentProfile]:
        
        query  = session.query(StudentProfile)
        if first_name:
            query = query.filter(StudentProfile.first_name.ilike(f"%{first_name}%"))
        if college_name:
            query = query.filter(StudentProfile.college_name.ilike(f"%{college_name}%"))
        if branch:
            query = query.filter(StudentProfile.branch.ilike(f"%{branch}%"))
        if semester is not None:
            query = query.filter(StudentProfile.semester == semester)
        if gender is not None:
            query = query.filter(StudentProfile.gender == gender)
        if sort_by:
            column = getattr(StudentProfile, sort_by)
            if order.lower() == "desc":
                query = query.order_by(desc(column))
            else:
                query = query.order_by(column)
        else:
            query = query.order_by(desc(StudentProfile.id))
                
        
        
        students = query.offset(offset).limit(size).all()
        return students
