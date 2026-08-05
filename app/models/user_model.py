from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.session import Base
from app.models.application_model import Application
from app.models.olympiad_model import Olympiad
from app.models.refresh_token_model import RefreshToken
from app.models.student_profile_model import StudentProfile


class UserRole(str , Enum):
    ADMIN = "admin"
    STUDENT = "student"
    SUPER_ADMIN = "super_admin"
    

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
        index=True
    )
    password_hash:Mapped[str] = mapped_column(
        nullable=False
    )
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole),
                                        default=UserRole.STUDENT)
    is_active:Mapped[bool] = mapped_column(
        default=True
    )

    created_at:Mapped[datetime] = mapped_column(DateTime,server_default=func.now())

    updated_at:Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),onupdate=func.now())
    
    created_olympiads:Mapped[list["Olympiad"]] = relationship(back_populates="creator")
    
    applications:Mapped[list["Application"]] = relationship(back_populates="user")
    
    student_profile:Mapped["StudentProfile"] = relationship(back_populates="user",uselist=False,cascade="all, delete-orphan")
    
    refresh_tokens:Mapped[list["RefreshToken"]] =  relationship(back_populates="user",cascade="all, delete-orphan")