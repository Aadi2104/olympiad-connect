from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ApplicationStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    


class Application(Base):
    __tablename__="applications"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "olympiad_id",
            name = "uq_user_olympiad"
        ),
    )
    id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),nullable=False)
    olympiad_id:Mapped[int]=mapped_column(ForeignKey("olympiads.id"),nullable=False)
    status:Mapped[ApplicationStatus] = mapped_column(SqlEnum(ApplicationStatus),default=ApplicationStatus.PENDING)
    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now())
    updated_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),onupdate=func.now())
    user:Mapped["User"]=relationship(back_populates="applications")
    olympiad:Mapped["Olympiad"]=relationship(back_populates="applications")
    
    
    