from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column , relationship
from enum import Enum
from sqlalchemy import DateTime,ForeignKey,Enum as SqlEnum
from datetime import datetime
from typing import List
from sqlalchemy.sql import func

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
    
    created_olympiads:Mapped[List["Olympiad"]] = relationship(back_populates="creator")
    
    applications:Mapped[List["Application"]] = relationship(back_populates="user")
    
    student_profile:Mapped["StudentProfile"] = relationship(back_populates="user",uselist=False,cascade="all, delete-orphan")