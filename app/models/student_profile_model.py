from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum as SqlEnum, DateTime, func
from datetime import date, datetime
from enum import Enum


class StudentGender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    first_name: Mapped[str] = mapped_column(index=True)

    last_name: Mapped[str] = mapped_column(index=True)
    
    gender: Mapped[StudentGender] = mapped_column(SqlEnum(StudentGender))

    date_of_birth: Mapped[date] = mapped_column(nullable=False)

    college_name: Mapped[str] = mapped_column(nullable=False)

    semester: Mapped[int] = mapped_column(nullable=False)

    enrollment_number: Mapped[str] = mapped_column(unique=True, index=True)

    branch: Mapped[str] = mapped_column()

    phone_number: Mapped[str] = mapped_column(unique=True, index=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="student_profile")
